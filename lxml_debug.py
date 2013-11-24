#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (c) Nikita Kovaliov, maizy.ru, 2013
# The MIT License, see LICENSE.txt for details.

from __future__ import unicode_literals, absolute_import, print_function

import sys
import os
import random
import cPickle as pickle
import base64

from lxml import etree

__version__ = '0.0-proof-of-concept'

# TODOs:
#  * эмулировать файловые объекты, для вывода ошибок в XSLT с файлом и строкой
#  * opt parse
#  * output dumping ("-o")
#  * параметр "--base-path" для resolver, запрещающий выход за её пределы
#  * параметр "--dump-results" для сохранения в output обработанных xsl
#  * пофиксить и дополнить panforte-path шаблон
#    * добавлять и строить динамечески (до xsl:output если есть, либо в конец)
#    * добавлять случайный префикс к названию
#    * в debug-path выводить полный путь (сейчас только на 1 уровень выше)
#    * можно ли получить полный путь до контекста в именных шаблонах?
#  * logging
#  * api: возврат всех результатов в виде объектов (list'ы из namedtuple)
#    * xml вывод из результатов
#    * html отчёт из результатов
#  * api: хуки для пре/пост процессинга xsl, data xml, результатов
#  * подмешивать результаты стд. xslt профайлера
#  * unit тесты
#  * python 2.6, 2.7, 3.2, 3.3 support
#  * lxml 2.x & 3.x support
#  * оптимизация процессинга по времени и расходу памяти

dump_output = False


def main(argv):
    if len(argv) < 3:  # TODO: opt parse
        sys.stderr.write('Usage {0}: xsl_file data_file\n'.format(argv[0]))
        return 2
    xsl_file = argv[1]
    data_file = argv[2]
    assert os.path.isfile(xsl_file)
    assert os.path.isfile(data_file)
    return debug(xsl_file, data_file)


def _title(text):
    print('{0} {1} {0}'.format('=' * 8, text))


def _log(text):
    print('> ' + text)

XSL_NS = 'http://www.w3.org/1999/XSL/Transform'
NSMAP = {'xsl': XSL_NS}
XSL_TAG = '{' + XSL_NS + '}'

# FIXME: tmp
output_strip = os.path.abspath(os.path.dirname(__file__))
output_files = os.path.join(os.path.dirname(__file__), 'output')


def encode(debug_data):
    return base64.encodestring(pickle.dumps(debug_data))


def decode(encoded_debug_data):
    return pickle.loads(base64.decodestring(encoded_debug_data))


def add_xsl_debug_info(tree, file_name, prefix):
    for t_xml in tree.getroot().xpath('//xsl:template', namespaces=NSMAP):
        dbg_xml = etree.Element('{0}message'.format(XSL_TAG))
        debug_data = {
            b'l': t_xml.sourceline,
            b'f': file_name,
            b'n': t_xml.get('name'),
            b'm': t_xml.get('mode'),
            b'mt': t_xml.get('match'),
        }
        dbg_xml.text = '{0}|{1}|'.format(prefix, encode(debug_data))
        etree.SubElement(dbg_xml, '{0}apply-templates'.format(XSL_TAG), select='.', mode='panforte-path')
        after = None
        for ch in t_xml.iterchildren():  # TODO: optimize
            if ch.tag in ('{0}param'.format(XSL_TAG), '{0}variable'.format(XSL_TAG), etree.Comment):
                after = ch
        if after is not None:
            after.addnext(dbg_xml)
        else:
            t_xml.insert(0, dbg_xml)


def dump_xsl(url, content):
    rel = os.path.relpath(url, output_strip)
    res_path = os.path.join(output_files, rel)
    try:
        os.makedirs(os.path.dirname(res_path))
    except OSError:
        pass
    with open(res_path, 'w') as f:
        f.write(content)


class PanforteResolver(etree.Resolver):

    def __init__(self, prefix):
        super(PanforteResolver, self).__init__()
        self._prefix = prefix
        self.clean_up()

    def clean_up(self):
        self._processed = {}

    def resolve(self, url, pubid, context):
        if url not in self._processed:
            _log('processing {0}'.format(url))
            with open(url, 'r') as f:
                tree = etree.parse(f)
            add_xsl_debug_info(tree, url, self._prefix)
            res = etree.tostring(tree, encoding=unicode).encode('utf-8')

            # FIXME: tmp
            if dump_output:
                dump_xsl(url, res)

            self._processed[url] = res
        else:
            _log('reuse {0}'.format(url))
        return self.resolve_string(string=self._processed[url], context=context)


def debug(xsl_file, data_file):

    _title('XSL FILE')
    print(xsl_file)

    _title('DATA FILE')
    print(data_file)

    prefix = 'panforte{0}'.format(random.randint(10000, 99999))
    xsl_preprocessed = etree.parse(open(xsl_file, 'r'))
    add_xsl_debug_info(xsl_preprocessed, xsl_file, prefix)
    xsl_preprocessed = etree.tostring(xsl_preprocessed, encoding=unicode).encode('utf-8')

    # TODO: вставлять и собирать динамически
    path_debug = open('path.xsl', 'r').read()
    xsl_preprocessed = xsl_preprocessed.replace('<xsl:output', path_debug + '<xsl:output')

    _title('preprocessed root xsl')
    if dump_output:
        dump_xsl(os.path.abspath(xsl_file), xsl_preprocessed)

    parser = etree.XMLParser()
    parser.resolvers.add(PanforteResolver(prefix))
    xsl = etree.fromstring(xsl_preprocessed, parser=parser, base_url=os.path.abspath(xsl_file))

    data = etree.parse(open(data_file, 'r'))
    transform = etree.XSLT(xsl)
    try:
        result = transform(data, profile_run=True)
    except etree.XSLTApplyError as e:
        _title('XSLT Error')
        print(e)
        return 1

    _title('RESULTS')
    print(result)

    _title('PROFILE')
    print(etree.dump(result.xslt_profile.getroot()))

    _title('MESSAGES')
    for entry in transform.error_log:
        mes = entry.message
        if mes.startswith(prefix):
            parts = mes.split('|', 3)
            debug_info = decode(parts[1])
            if debug_info['m'] is None and debug_info['mt'] is None:
                tpl = 'NAMED TPL: context="{c}", name="{n}", file="{f}:{l}"'
            else:
                tpl = 'TPL: context="{c}", mode="{m}", match="{mt}", file="{f}:{l}"'
            print(tpl.format(c=parts[2], **debug_info))
        else:
            print('MSG: mes="{en.message}", column="{en.column}", file="{en.filename}:{en.line}"'
                  .format(en=entry))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
