#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.text import TextManager
tm = TextManager('errors')


class BotError(Exception):
    def __init__(self, error_code, **kwargs):
        self.error_code = error_code
        self.message = tm.get(error_code, **kwargs)

    def __str__(self):
        return self.message


class NoActionError(Exception):
    def __init__(self, action, arguments):
        self.action = action
        self.arguments = arguments

    def __str__(self):
        return self.action + ':' + str(self.arguments)
