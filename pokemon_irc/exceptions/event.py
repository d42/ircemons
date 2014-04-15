#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.text import TextManager
tm = TextManager('errors')


class EventError(Exception):
    def __init__(self, error_code, **kwargs):
        self.message = tm.get(error_code, **kwargs)

    def __str__(self):
        return self.message
