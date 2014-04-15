#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.exceptions.text import NoTextError, NoTextVarError
errors = {
    "nouser": "No such user: {name}.",
    "nopokemon": "Player {name} doesn't have pokemon called {pokename}.",
    "alreadyreg": "User {name} is already registered.",
    "shortpass": "Password is shorter than {length} characters",
    "badpassword": "No such user or bad password.",
    "alreadypokemon": "Pokemon with name {name} already exists.",
    "alreadysummoned": "One is enough"
}

pokemon_details = (
    "[{p.base_pokemon}|{p.name}], [hp:{p.current_hp}/{p.hp}, att:{p.attack}, "
    "def:{p.defence}, sp att:{p.special_attack}, sp def:{p.special_defence}, "
    "speed:{p.speed}, level:{p.level}] {p.known_moves}"
)

action_responses = {
    "okauth": "Authorized.",
    "noauth": "Not authorized",
    "alreadyauth": "Already authorized",
    "onchallenge": "Player {name} has been challenged.",
    "uhoh": "Something went wrong.",
    "absent": "Player {name} is not on the main channel.",
    "challenge": "{name} has challenged you to a battle!",
    "muchrequest": "There's more than one request, specify player.",
    "nocommand": "No such command.",
    "onsummon": "{pokename}, i choose you!",
    "notyourturn": "It's not your turn.",
    "notyourbattle": "It's not your battle."
}


class TextManager:

    def __init__(self, text_set_name):
        self.text_set = globals()[text_set_name]  # XXX:

    def get(self, code, **kwargs):
        text = self.text_set.get(code, None)
        if not text:
            raise NoTextError(code)

        try:
            text = text.format(**kwargs)
        except KeyError as e:
            raise NoTextVarError(code, e)

        return text
