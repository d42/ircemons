#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import nose
import mock

from pokemon_irc import pokedb


def derp(url):
    pass


@mock.patch("pokedb.request_table")
def test_types(derp):
    pokemon_irc.pokedb.poke_get(pokemon_irc.pokedb.types)
