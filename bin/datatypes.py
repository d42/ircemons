#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import namedtuple
from urls import *

#types = {
    #normal
    #fire
    #water
    #electric
    #grass
    #ice
    #fighting
    #poison
    #ground
    #flying
    #psychic
    #bug
    #rock
    #ghost
    #dragon
    #dark
    #steel
    #fairy
#}


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
    [ability, ability_defaults, POKEDB_ABILITIES_URL],
    [move, move_defaults, POKEDB_MOVES_URL],
    [entry, entry_defaults, POKEDB_POKEMON_URL],
]
for tup, d, url in triples:
    tup.defaults = d
    tup.url = url
