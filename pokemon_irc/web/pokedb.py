#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from itertools import zip_longest, product
from collections import defaultdict
import requests
import lxml.html


def get_columns(row, datatype):
    ret_list = []

    def get(e, d):
        if not e: return d
        if type(d) == list: # such list wow 
            return [e[0].strip()] if len(e) == 1 else e

        if type(d) == int:
            return e[0].strip() if e[0].strip() == '-' else int(e[0])

        return type(d)(e[0].strip())

    for (col, val) in zip_longest(row, datatype.defaults):
        ret_list.append(get(col.xpath('.//text()'), val))
    return ret_list


def request_table(url):
    text = requests.get(url).text
    return lxml.html.fromstring(text)


def poke_get(datatype):
    tree = request_table(datatype.url)

    def parse_row(row):
        return get_columns(row, datatype)

    for row in tree.xpath('//tbody/tr'):
        yield datatype(*parse_row(row))


def poke_get_type_damage(datatype):
    tree = request_table(datatype.url)

    def parse_row(row):
        return get_columns(row, datatype)

    matrix = [parse_row(row[1:]) for row in tree.xpath('//tbody/tr')]
    damage = defaultdict(set)
    damage_translation = {'½': 0.5, '2': 2, '0': 0}

    for (i, j) in product(range(len(datatype)), repeat=2):
        val = matrix[i][j]
        if val == 1: continue
        typei, typej = datatype[i], datatype[j]
        damage[typei].add((typej, damage_translation.get(val, 1)))
    return damage
