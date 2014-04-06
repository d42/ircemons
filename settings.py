#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pokemons.db')

#urls with pokemans features
POKEDB_POKEMON_URL = "http://pokemondb.net/pokedex/all"
POKEDB_MOVES_URL = "http://pokemondb.net/move/all"
POKEDB_ABILITIES_URL = "http://pokemondb.net/ability"
POKEDB_TYPE_CHART_URL = "http://pokemondb.net/type"
