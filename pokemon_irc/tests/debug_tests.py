#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from debug import *
from collections import deque

tests = [
    (create_player  , "create player jp2gmd"          ),
    (create_pokemon , "create pokemon jp2gmd pikachu" ),
    (list_pokemons  , "list pokemons jp2gmd"          ),
    (list_players   , "list players"                  ),
    (list_moves     , "list moves 1"                  ),
    (evolve_pokemon , "evolve 1"                      ),
    (change_stat    , "change stat 1 hp 200"          ),
    (del_pokemon    , "del pokemon 1"                 ),
    (del_player     , "del player 1"                  ),
]



def test_debug():

    for func, test in tests:
        test = deque(test.split())
        state = debug_functions

        while test:
            state = state[test.popleft()]
            if hasattr(state, '__call__'):
                #assert(state == func)
                state(*test)
                break



