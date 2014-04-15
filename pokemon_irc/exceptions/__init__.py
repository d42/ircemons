#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.text import errors

successes = {}


class EventError(Exception):
    def __init__(self, error_code, **kwargs):
        self.message = errors[error_code].format(**kwargs)

    def __str__(self):
        return self.message


class NoTextError(Exception):
    def __init__(self, error_code, **kwargs):
        self.code = error_code

    def __str__(self):
        return self.code
