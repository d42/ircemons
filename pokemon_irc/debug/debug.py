#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from pokemon_irc.exceptions.debug import debug_exception
from pokemon_irc.game import events
from pokemon_irc import settings
import socket
from collections import deque


def create_player(player_name, password):
    return events.create_player(player_name, password)


def create_pokemon(player_name, pokemon_name):
    return events.create_pokemon(player_name, pokemon_name)


def list_all_pokemons():
    pokemons = session.query(orm.PlayerPokemon).all()
    return "\n".join("%s %s" % (p.id, p.name) for p in pokemons)


def list_pokemons(player_name=None):
    if not player_name: return list_all_pokemons()
    return events.list_pokemons(player_name)


def list_players():

    for x in session.query(orm.Player).all():
        print(x.id, x.name)
    return  ''


def list_all_moves():
    for move in session.query(orm.Move).all():
        print(move.id, move.name, move.effect, sep='\t')


def list_moves(pokemon_name=None):
    if not pokemon_name:
        return list_all_moves()

    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    if not pokemon:
        return "No such pokemon id"
    return "\n".join(move.name for move in pokemon.known_moves)


def add_move(pokemon_id, move_id):
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    move = session.query(orm.Move).filter_by(id=move_id).first()
    session.add(orm.KnownMove(pokemon_id=pokemon.id, move_id=move.id))
    session.commit()

    return "{} got some {}!".format(pokemon.name, move.name)


def del_pokemon(pokemon_id):
    return events.del_pokemon(pokemon_id)


def del_player(player_name):
    player = session.query(orm.Player).filter_by(name=player_name).first()
    if not player: return "No such player"
    player_name = player.name

    for pokemon in player.pokemons:
        print('\t', del_pokemon(pokemon.id))
    session.delete(player)
    session.commit()

    return "{} dies".format(player_name)


def add_xp(pokemon_id, xp=100):
    xp = int(xp)
    return '%s %s' % events.add_xp(pokemon_id, xp)


def evolve_pokemon(pokemon_id):
    pass


def change_stat(pokemon_id, stat, new_value):
    pass


def info_player(player_id):
    pass


def info_pokemon(pokemon_id):
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    params = [x for x in dir(pokemon) if not x.startswith('_')]

    return '\n'.join("%s=%s" % (x, getattr(pokemon, x)) for x in params)


def call_server(*tokens):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(settings.SOCKET_PATH)
    channel = settings.IRC_MAIN_CHANNEL,

    s.sendall(bytes(' '.join(channel + tokens), encoding="utf-8"))
    return "ok"


def call_battle(*tokens):
    pass

debug_functions = {
    'create': {'pokemon': create_pokemon, 'player': create_player},
    'list': {'pokemons': list_pokemons, 'players': list_players, 'moves': list_moves},
    'info': {'player': info_player, 'pokemon': info_pokemon},
    'add': {'move': add_move, 'xp': add_xp},
    'del': {'pokemon': del_pokemon, 'player': del_player},
    'change': {'stat': change_stat},
    'evolve': evolve_pokemon,
    'server': call_server,
    'battle': call_battle
}
