#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import namedtuple, UserList
from pokemon_irc.settings import settings
pokedb_settings = settings["pokedb"]

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


pokemon_defaults = [0, '', [], 0, 0, 0, 0, 0, 0, 0]
pokemon = namedtuple(
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

pokemon.classes = 'data-table'

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

move_level.xpath = "//li[@id='svtabs_moves_13']//table[1]/tbody/tr"
move_level.url = 'http://pokemondb.net/pokedex/{name}'


triples = [
    [ability, ability_defaults, pokedb_settings["abilities"]],
    [move, move_defaults, pokedb_settings["moves"]],
    [pokemon, pokemon_defaults, pokedb_settings["pokemons"]],
    [move_level, move_level_defaults, pokedb_settings["pokemon"]],
    [types, [1.0] * len(types), pokedb_settings["types"]]
]
for type, d, url in triples:
    type.defaults = d
    type.url = url
