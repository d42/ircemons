#!/usr/bin/env python
# -*- encoding: utf-8 -*-

errors = {
    "nouser": "No such user: {name}.",
    "nopokemon": "Player {name} doesn't have pokemon called {pokename}.",
    "alreadyreg": "User {name} is already registered.",
    "shortpass": "Password is shorter than {length} characters",
    "badpassword": "No such user or bad password.",
    "alreadypokemon": "Pokemon with name {name} already exists."
}

pokemon_details = (
    "[{p.base_pokemon}|{p.name}], [hp:{p.current_hp}/{p.hp}, att:{p.attack}, "
    "def:{p.defence}, sp att:{p.special_attack}, sp def:{p.special_defence}, "
    "speed:{p.speed}, level:{p.level}] {p.known_moves}"
)

action_response = {
    'okauth': "Authorized.",
    "alreadyauth": "Already authorized",
    "onchallenge": "Player {name} has been challenged.",
    "uhoh": "Something went wrong.",
    "absent": "Player {name} is not on the main channel.",
    "challenge": "{name} has challenged you to a battle!",
    "muchrequest": "There's more than one request, specify player.",
    "nocommand": "No such command.",
    "onsummon": "{pokename}, i choose you!"
}
