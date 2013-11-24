#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Copyright (c) Nikita Kovaliov, maizy.ru, 2013
# See LICENSE.txt for details.

from __future__ import unicode_literals, absolute_import, print_function

import sys
import os

from lxml import etree


def _title(text):
    print('{0} {1} {0}'.format('=' * 8, text))


def apply_xsl(xsl_file, data_file):
    _title('XSL FILE')
    print(xsl_file)

    _title('DATA FILE')
    print(data_file)

    data = etree.parse(open(data_file, 'r'))
    xsl = etree.parse(open(xsl_file, 'r'))

    transform = etree.XSLT(xsl)
    try:
        result = transform(data)
    except etree.XSLTApplyError as e:
        _title('XSLT Error')
        print(e)
        print('{e.filename}:{e.line}'.format(e=e.error_log.last_error))
        return 1

    _title('RESULTS')
    print(result)

    _title('MESSAGES')
    for entry in transform.error_log:
        print('message from line {en.line}, col {en.column}, file {en.filename}: {en.message}'
              .format(en=entry))
        print()


def main(argv):
    if len(argv) < 3:  # TODO: opt parse
        sys.stderr.write('Usage {}: xsl_file data_file\n'.format(argv[0]))
        return 2
    xsl_file = argv[1]
    data_file = argv[2]
    assert os.path.isfile(xsl_file)
    assert os.path.isfile(data_file)
    apply_xsl(xsl_file, data_file)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
