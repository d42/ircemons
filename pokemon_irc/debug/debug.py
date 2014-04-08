#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from models import orm
from exceptions.debug import debug_exception


def create_player(player_name):
    print("jp2gmd")
    raise(debug_exception)
    pass


def create_pokemon(player_name, pokemon_name):
    pass


def list_pokemons(player_name):
    pass


def list_players():
    pass


def list_moves(pokemon_id):
    pass


def add_move(pokemon_id, move_name):
    pass


def del_pokemon(pokemon_id):
    pass


def del_player(player_id):
    pass


def evolve_pokemon(pokemon_id):
    pass


def change_stat(pokemon_id, stat, new_value):
    pass


debug_functions = {
    'create': {'pokemon': create_pokemon, 'player': create_player},
    'list': {'pokemons': list_pokemons, 'players': list_players, 'moves': list_moves},
    'add': {'move': add_move},
    'del': {'pokemon': del_pokemon, 'player': del_player},
    'change': {'stat': change_stat},
    'evolve': evolve_pokemon,
}
