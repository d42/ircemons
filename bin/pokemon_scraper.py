#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from itertools import zip_longest
import requests
import lxml.html
import csv
import logging
from datatypes import entry, move, ability
logging.basicConfig(level=logging.INFO)


def get_columns(row, type):
    ret_list = []

    def get(e, d):
        if not e: return d
        return e[0].strip()

    for (col, val) in zip_longest(row, type.defaults):
        ret_list.append(get(col.xpath('.//text()'), val))
    return ret_list


def poke_get(type):
    text = requests.get(type.url).text
    tree = lxml.html.fromstring(text)

    def parse_row(row):
        return get_columns(row, type)

    for row in tree.xpath('//tbody/tr'):
        yield parse_row(row)

actions = {
    "moves.csv": move,
    "pokemons.csv": entry,
    "abilities.csv": ability
}


def main():
    for (file, type) in actions.items():
        logging.info("downloading %s content..." % file)
        with open(file, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(poke_get(type))

if __name__ == '__main__':
    main()
