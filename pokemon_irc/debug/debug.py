#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.models import orm
from sqlalchemy.orm import sessionmaker
from pokemon_irc.exceptions.debug import debug_exception
import settings
Session = sessionmaker(bind=orm.engine)
session = Session()


def create_player(player_name):
    session.add(orm.Player(name=player_name))
    session.commit()

    return "OK"


def create_pokemon(player_id, pokemon_name):
    name = session.query(orm.Player).filter_by(id=player_id).first().name
    if not name: return "w0t m8"
    
    n = pokemon_name.capitalize()
    session.query()
    p = session.query(orm.Pokemon).filter_by(name=n).first()
    pp = orm.PlayerPokemon(
        name=("{}'s {}".format(name,p.name)),
        player_id=player_id,
        hp=p.hp,
        attack=p.attack,
        defence=p.defence,
        special_attack=p.special_attack,
        special_defence=p.special_defence,
        speed=p.speed,
    )
    session.add(pp)
    session.commit()


def list_pokemons(player_id):
    player = session.query(orm.Player).filter_by(id=player_id).first()
    if not player: return "No such player id"
    for p in player.pokemons:
        print(p.id, p.name)



def list_players():
    for x in session.query(orm.Player).all():
        print(x.id, x.name)
    pass

def list_all_moves():
    for move in session.query(orm.Move).all():
        print(move.id, move.name)

def list_moves(pokemon_id=None):
    if not pokemon_id: return list_all_moves()

    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    if not pokemon: return "No such pokemon id"
    return "\n".join(move.name for move in pokemon.known_moves)


def add_move(pokemon_id, move_id):
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    move = session.query(orm.Move).filter_by(id=move_id).first()
    session.add(orm.KnownMove(pokemon_id=pokemon.id, move_id=move.id))
    session.commit()

    return "{} got some {}!".format(pokemon.name, move.name)


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
