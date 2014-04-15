#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.text import errors


class EventError(Exception):
    def __init__(error_code, **kwargs):
        return errors[error_code].format(**kwargs)
