#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import namedtuple, UserList
from pokemon_irc import settings

types = UserList([
    'normal',
    'fire',
    'water',
    'electric',
    'grass',
    'ice',
    'fighting',
    'poison',
    'ground',
    'flying',
    'psychic',
    'bug',
    'rock',
    'ghost',
    'dragon',
    'dark',
    'steel',
    'fairy',
])


entry_defaults = [0, '', [], 0, 0, 0, 0, 0, 0, 0]
entry = namedtuple(
    'pokemon',
    [
        'id',
        'name',
        'types',
        'total',
        'hp',
        'attack',
        'defence',
        'special_attack',
        'special_defence',
        'speed'
    ]
)

entry.classes = 'data-table'

move_defaults = ['', '', '',  0, 0, 0, '', '', 0]
move = namedtuple(
    'move',
    [
        'name',
        'type',
        'category',
        'power',
        'accuracy',
        'pp',
        'tm',
        'effect',
        'effect_prob'
    ]
)


ability_defaults = ['', 0, '', 0]
ability = namedtuple(
    "ability",
    [
        'name',
        'pokemon',
        'description',
        'gen'
    ])


move_level_defaults = [1, '']
move_level = namedtuple(
    "move_level",
    [
        "level",
        "name"
    ]
)

#move_level.xpath = "//div[@class='col desk-span-6 lap-span-12'][1]/table[1]/tbody/tr"
move_level.xpath = "//li[@id='svtabs_moves_13']//table[1]/tbody/tr"
move_level.url = 'http://pokemondb.net/pokedex/{name}'


triples = [
    [ability, ability_defaults, settings.POKEDB_ABILITIES_URL],
    [move, move_defaults, settings.POKEDB_MOVES_URL],
    [entry, entry_defaults, settings.POKEDB_POKEMONS_URL],
    [move_level, move_level_defaults, settings.POKEDB_POKEMON_URL],
    [types, [1.0] * len(types), settings.POKEDB_TYPE_CHART_URL]
]
for type, d, url in triples:
    type.defaults = d
    type.url = url
