#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from itertools import product, zip_longest
from collections import defaultdict
from httpcache import CachingHTTPAdapter
import requests
import logging

import lxml.html



class PokeDBMachine:
    def __init__(self):
        session = requests.session()

    def get_columns(self, row, datatype):
        ret_list = []
        specials = {'½': 0.5, '2': 2, '0': 0, '∞': 9001, '-': 9002}

        def get(val, def_val):
            if not def_val:
                return val

            if not val:
                return def_val

            val0 = val[0].strip()
            if type(def_val) == str:
                return val0

            if type(def_val) == list:
                return [val0] if len(val) == 1 else val

            if type(def_val) == int:
                return int(specials.get(val0, val0))

            if type(def_val) == float:
                return float(specials.get(val0, val0))

            return type(def_val)(val0)

        for (col, val) in zip_longest(row, datatype.defaults):
            ret_list.append(get(col.xpath('.//text()'), val))
        return ret_list

    def request_table(self, url, classes="data-table wide-table", xpath=None):
        if not xpath:
            xpath = "//table[@class='{}'][1]/tbody/tr".format(classes)

        r = session.get(url)
        r.encoding = 'utf-8'
        text = r.text
        tree = lxml.html.fromstring(text)
        table = tree.xpath(xpath)
        return table

    def poke_get(self, datatype, **kwargs):
        if kwargs:
            url = datatype.url.format(**kwargs)
        else:
            url = datatype.url

        if hasattr(datatype, 'xpath'):
            table = request_table(url, xpath=datatype.xpath)

        elif hasattr(datatype, 'classes'):
            table = request_table(url, classes=datatype.classes)

        else:
            table = request_table(url)

        def parse_row(row):
            return get_columns(row, datatype)

        for row in table:
            yield datatype(*parse_row(row))

    def poke_get_type_damage(self, datatype):
        table = request_table(datatype.url, classes="type-table")

        def parse_row(row):
            return get_columns(row, datatype)

        matrix = [parse_row(row[1:]) for row in table]
        damage = defaultdict(dict)

        for (i, j) in product(range(len(datatype)), repeat=2):
            val = matrix[i][j]
            if val == 1:
                continue

            typei, typej = datatype[i], datatype[j]
            damage[typei][typej] = val
        return damage
