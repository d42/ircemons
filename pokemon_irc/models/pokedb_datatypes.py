#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import namedtuple, UserList
import settings

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


entry_defaults = ['', '', 0, 0, 0, 0, 0, 0, 0, 0]
entry = namedtuple(
    'pokemon',
    [
        'name',
        'type',
        'id',
        'total',
        'hp',
        'attack',
        'defense',
        'special_attack',
        'special_defence',
        'speed'
    ]
)

move_defaults = ['', '', '',  0, 0, 0, 0, '', 0]
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


ability_defaults = ['', 0, 0]
ability = namedtuple(
    "ability",
    [
        'name',
        'pokemon',
        'description',
        'gen'
    ])

triples = [
    [ability, ability_defaults, settings.POKEDB_ABILITIES_URL],
    [move, move_defaults, settings.POKEDB_MOVES_URL],
    [entry, entry_defaults, settings.POKEDB_POKEMON_URL],
    [types, [1] * len(types), settings.POKEDB_TYPE_CHART_URL]
]
for type, d, url in triples:
    type.defaults = d
    type.url = url
