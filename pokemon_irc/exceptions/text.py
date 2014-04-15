#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class NoTextError(Exception):
    def __init__(self, error_code):
        self.code = error_code

    def __str__(self):
        return self.code


class NoTextVarError(Exception):
    def __init__(self, error_code, arg):
        self.code = error_code
        self.arg = arg

    def __str__(self):
        return ':'.join(self.code, self.arg)
