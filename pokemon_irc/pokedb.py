#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from itertools import zip_longest, product
from collections import defaultdict
import requests
import lxml.html
from . models.pokedb_datatypes import entry, move, ability, types


def get_columns(row, datatype):
    ret_list = []

    def get(e, d):
        if not e: return d
        return e[0].strip()

    for (col, val) in zip_longest(row, datatype.defaults):
        ret_list.append(get(col.xpath('.//text()'), val))
    return ret_list


def poke_get(datatype):
    text = requests.get(datatype.url).text
    tree = lxml.html.fromstring(text)

    def parse_row(row):
        return get_columns(row, datatype)

    for row in tree.xpath('//tbody/tr'):
        yield datatype(*parse_row(row))


def poke_get_type_damage(datatype=types):
    text = requests.get(datatype.url).text
    tree = lxml.html.fromstring(text)

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