# coding=utf-8

from lxml import etree
from tornado.escape import json_encode


def _escape(value):
    return json_encode(value)[1: -1] if value else ''


def escape_json(_, value):
    if isinstance(value, list):
        if not value:
            return ''

        value = value[0].text if etree.iselement(value[0]) else value[0]

    return _escape(value)


def etree_enrich_hh_namespace():
    ns = etree.FunctionNamespace('http://schema.reintegration.hh.ru/types')
    ns.prefix = 'hh'

    ns['escape-json'] = escape_json
