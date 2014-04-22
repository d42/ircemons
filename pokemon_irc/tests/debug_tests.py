#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from sqlalchemy import create_engine
from pokemon_irc.models import orm
from pokemon_irc.debug import *
from collections import deque

from pokemon_irc.settings import settings

tests = [
    (create_player  , "create player jp2gmd password" ),
    (create_pokemon , "create pokemon jp2gmd pikachu" ),
    (list_pokemons  , "list pokemons jp2gmd"          ),
    (list_players   , "list players"                  ),
    (list_moves     , "list moves jp2gmd pikachu"     ),
    (evolve_pokemon , "evolve 1"                      ),
    (change_stat    , "change stat 1 hp 200"          ),
    (del_pokemon    , "del pokemon 1"                 ),
    (del_player     , "del player jp2gmd"             ),
]


def setup():
    db_uri = settings['game']['database_uri']
    engine = create_engine('sqlite://')
    session.bind = engine

    orm.Base.metadata.create_all(engine)
    session.execute('ATTACH DATABASE "%s" as derp' % db_uri[10:])
    session.execute('INSERT INTO pokemon SELECT * from derp.pokemon')

def test_paths():

    for func, test in tests:
        test = deque(test.split())
        state = debug_functions

        print(test)
        while test:
            state = state[test.popleft()]
            if hasattr(state, '__call__'):
                state(*test)
                break


def test_create_player():
    assert not session.query(orm.Player).filter_by(name="jp2gmd").first()
    create_player("jp2gmd", "password")
    session.commit()
    assert session.query(orm.Player).filter_by(name="jp2gmd").first()


def test_create_pokemon():
    assert not session.query(orm.PlayerPokemon).filter_by(name="pikachu").first()
    create_pokemon("jp2gmd", "pikachu")
    session.commit()
    assert session.query(orm.PlayerPokemon).filter_by(name="pikachu").first()


def test_list_pokemons():
    assert list(list_pokemons("jp2gmd")) == 1


def test_list_moves():




