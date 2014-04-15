#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import nose
from mock import patch
import os.path
import lxml.html
from models.pokedb_datatypes import move, entry, ability, types
import settings


data_files = {
    settings.POKEDB_MOVES_URL: 'data/moves',
    settings.POKEDB_POKEMON_URL: 'data/pokemons',
    settings.POKEDB_ABILITIES_URL: 'data/abilities',
    settings.POKEDB_TYPE_CHART_URL: 'data/types'
}
import web

current_dir = os.path.dirname(__file__)

def request_stub(url):
    with open(os.path.join(current_dir, data_files[url])) as file:
        return lxml.html.fromstring(file.read())





@patch("web.pokedb.request_table", new=request_stub)
def test_pokedb_moves():
    a = move(name='derpderp', type='Grass', category='Special', power=20, accuracy=100, pp=25, tm='', effect='User recovers half the HP inflicted on opponent.', effect_prob='-')
    asd = next(web.poke_get(move))
    assert a == asd

@patch("web.pokedb.request_table", new=request_stub)
def test_pokedb_pokemons():
    a = entry(id=1, name='Bulbasaur', type=['Grass', 'Poison'], total=318, hp=45, attack=49, defense=49, special_attack=65, special_defence=65, speed=45)
    asd = next(web.poke_get(entry))
    assert a == asd

@patch("web.pokedb.request_table", new=request_stub)
def test_pokedb_abilities():
    a = ability(name='Adaptability', pokemon=9, description='Powers up moves of the same type.', gen=4)
    asd = next(web.poke_get(ability))
    assert a == asd
