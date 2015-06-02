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
import pprint

from lxml import etree

__version__ = '0.0-proof-of-concept'

# TODOs:
#  * эмулировать файловые объекты, для вывода ошибок в XSLT с файлом и строкой
#  * opt parse
#  * output dumping ("-o")
#  * параметр "--base-path" для resolver, запрещающий выход за её пределы
#  * параметр "--dump-results" для сохранения в output обработанных xsl (только с base-path)
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

dump_output = False  # XXX: не включать! не безопасно для примеров не из /samples


def main(argv):
    if len(argv) < 3:  # TODO: opt parse
        sys.stderr.write('Usage {0}: xsl_file data_file\n [--hh-exslt]'.format(argv[0]))
        return 2
    xsl_file = argv[1]
    data_file = argv[2]
    if len(argv) > 3 and argv[3] == '--hh-exslt':
        hh_exslt = True
    else:
        hh_exslt = False
    assert os.path.isfile(xsl_file)
    assert os.path.isfile(data_file)
    return debug(xsl_file, data_file, hh_exslt)


def _title(text):
    print('{0} {1} {0}'.format('=' * 8, text))


def _log(text):
    print('> ' + text)


def _strip_long_string(s, max_width=300):
    return s[:max_width-3] + '...' if len(s) > max_width else s

XSL_NS = 'http://www.w3.org/1999/XSL/Transform'
NSMAP = {'xsl': XSL_NS}
XSL_TAG = '{' + XSL_NS + '}'

PANFORTE_NS = 'https://github.com/maizy/panforte'
PANFORTE_TAG = '{' + PANFORTE_NS + '}'
PANFORTE_ALIAS = 'pn'
PANFORTE_NSMAP = {PANFORTE_ALIAS: PANFORTE_NS}

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
        etree.SubElement(dbg_xml, '{0}value-of'.format(XSL_TAG), select='pn:path(current())')

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
    _log('write xsl dump to {0}'.format(res_path))
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
            res = add_panforte_xmlns(res)  # FIXME: hack inside

            # FIXME: tmp
            if dump_output:
                dump_xsl(url, res)

            self._processed[url] = res
        else:
            _log('reuse {0}'.format(url))
        return self.resolve_string(string=self._processed[url], context=context)


def add_panforte_xmlns(result_string):
    #FIXME hack
    return result_string.replace(b'<xsl:stylesheet',
                                 b'<xsl:stylesheet xmlns:{0}="{1}" '.format(PANFORTE_ALIAS, PANFORTE_NS))


def print_path(context, element, **kwargs):
    el = element[0]  # FIXME: why??
    if isinstance(el, basestring):  # text nodes
        parent = el.getparent()
        return 'TEXT OF: ' + el.getparent().getroottree().getpath(parent)
    else:
        return el.getroottree().getpath(el)


def debug(xsl_file, data_file, hh_exslt=False):

    _title('XSL FILE')
    print(xsl_file)

    _title('DATA FILE')
    print(data_file)

    prefix = b'panforte{0}'.format(random.randint(10000, 99999))
    xsl = etree.parse(open(xsl_file, 'r'))

    add_xsl_debug_info(xsl, xsl_file, prefix)
    xsl_str = etree.tostring(xsl, encoding=unicode).encode('utf-8')
    xsl_str = add_panforte_xmlns(xsl_str)  # FIXME: hack inside

    _title('preprocessed root xsl')
    if dump_output:
        dump_xsl(os.path.abspath(xsl_file), xsl_str)

    parser = etree.XMLParser()
    parser.resolvers.add(PanforteResolver(prefix))
    # TODO: don't do tostring/fromstring mangling
    xsl_tree = etree.fromstring(xsl_str, parser=parser, base_url=os.path.abspath(xsl_file))

    data = etree.parse(open(data_file, 'r'))

    ns = etree.FunctionNamespace(PANFORTE_NS)
    ns.prefix = PANFORTE_ALIAS
    ns['path'] = print_path

    if hh_exslt:
        import hh_json
        hh_json.etree_enrich_hh_namespace()

    etree.XPathEvaluator(data, namespaces=PANFORTE_NSMAP)

    transform = etree.XSLT(xsl_tree)
    try:
        result = transform(data, profile_run=True)
    except etree.XSLTApplyError as e:
        _title('XSLT Error')
        print(e)
        print(e.__dict__)
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
            print(tpl.format(c=parts[2], **dict((k, _strip_long_string(v) if isinstance(v, basestring) else v)
                                                for k, v in debug_info.iteritems())))
        else:
            print('MSG: mes="{en.message}", column="{en.column}", file="{en.filename}:{en.line}"'
                  .format(en=entry))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
