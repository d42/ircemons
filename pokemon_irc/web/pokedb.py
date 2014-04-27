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

    def get_columns(self, row):


            return [get(val.xpath('.//text()'))
        for val in row]

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

    def poke_get(self, xpath, url, **kwargs):
        url = url.format(**kwargs)

        xpath = xpath
        table = self.request_table(url, xpath)

        def parse_row(row):
            return self.get_columns(row)

        for row in table:
            yield parse_row(row)
            #yield (parse_row(x for x in row)

    def poke_get_type_damage(self, datatype, **kwargs):
        url = datatype.url.format(**kwargs)
        xpath = datatype.xpath

        table = self.request_table(url, xpath)
        table_size = len(table)

        def parse_row(row):
            return self.get_columns(row, [float] * table_size)

        types = [row[0].text_content().lower() for row in table]
        matrix = [parse_row(row[1:]) for row in table]
        damage = defaultdict(dict)

        for (i, j) in product(range(len(matrix)), repeat=2):
            val = matrix[i][j]
            if val == 1 or not val:
                continue

            val = SPECIALS.get(val, val)

            typei, typej = types[i], types[j]
            yield datatype(typei, typej, val)

