#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from itertools import product, zip_longest
from collections import defaultdict
from httpcache import CachingHTTPAdapter
import requests
import logging

INF = 9001  # This would be over9000 anyway
MINUS = 9000
SPECIALS = {'½': 0.5, '2': 2, '0': 0, '∞': INF, '-': MINUS}

import lxml.html


class PokeDBMachine:
    def __init__(self):
        self.session = requests.session()
        self.cache = {}

    def get_columns(self, row, datatype):
        ret_list = []
        #specials = {'½': 0.5, '2': 2, '0': 0, '∞': INF, '-': MINUS}

        def get(val, def_val):
            if not def_val:
                return val

            if not val:
                return def_val()

            val0 = val[0].strip()
            if def_val == str:
                return val0

            if def_val == list:
                return [val0] if len(val) == 1 else val

            if def_val == int:
                return int(SPECIALS.get(val0, val0))

            if def_val == float:
                return float(SPECIALS.get(val0, val0))

            return def_val(val)

        for (col, val) in zip_longest(row, datatype.defaults):
            ret_list.append(get(col.xpath('.//text()'), val))
        return ret_list

    def request_table(self, url, xpath):

        text = self.cache.get(url, None)
        if not text:
            r = self.session.get(url)
            r.encoding = 'utf-8'
            text = r.text
            self.cache[url] = text

        tree = lxml.html.fromstring(text)
        table = tree.xpath(xpath)
        return table

    def poke_get(self, datatype, **kwargs):
        url = datatype.url.format(**kwargs)

        xpath = datatype.xpath
        table = self.request_table(url, xpath)

        def parse_row(row):
            return self.get_columns(row, datatype)

        for row in table:
            yield datatype(*parse_row(row))

    def poke_get_type_damage(self, datatype, **kwargs):
        url = datatype.url.format(**kwargs)
        xpath = datatype.xpath

        table = self.request_table(url, xpath)

        def parse_row(row):
            return self.get_columns(row, datatype)

        types = [row[0].text_content().lower() for row in table]
        matrix = [parse_row(row[1:]) for row in table]
        damage = defaultdict(dict)

        for (i, j) in product(range(len(matrix)), repeat=2):
            import ipdb; ipdb.set_trace()
            val = matrix[i][j]
            if val == 1 or not val:
                continue

            val = val[0]
            val = SPECIALS.get(val, val)

            typei, typej = types[i], types[j]
            yield datatype(typei, typej, val)

