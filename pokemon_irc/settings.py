#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'pokemons.db')

#urls with pokemans features
POKEDB_POKEMONS_URL = "http://pokemondb.net/pokedex/all"
POKEDB_MOVES_URL = "http://pokemondb.net/move/all"
POKEDB_ABILITIES_URL = "http://pokemondb.net/ability"
POKEDB_TYPE_CHART_URL = "http://pokemondb.net/type"
POKEDB_POKEMON_URL = "http://pokemondb.net/pokedex/{name}"


IRC_SERVER = "irc.freenode.net"
IRC_PORT = 6667
IRC_MAIN_CHANNEL = "#kekchan"
IRC_GM_NICK = "oakxDDDD"
IRC_REALNAME = "oak xDDDD"
IRC_OWNER = "DaZ"

IRC_BATTLE_CHANNEL_TEMPLATE = "#{name1}_vs_{name2}_{battle_id}"

