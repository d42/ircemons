#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
from os.path import dirname, abspath, join, isfile, expanduser
import configparser

class Config(configparser.RawConfigParser):

    def _validate_value_types(self, *, section="", option="", value=""):
        """ I like my ints, thank you very much"""
        return True

dotconfig = ".config/ircemons/settings.ini"
project_root = dirname(dirname(abspath(__file__)))
root = os.path.expanduser('~')

settings_path = join(project_root, "settings.ini")
if isfile(join(root, dotconfig)):
    settings_path = join(root, dotconfig)

settings = Config()
settings.read(settings_path)
db_uri = settings["game"]["database_uri"]

# expanduser reads only the first letter ;c
settings["game"]["database_uri"] = db_uri.replace('~', root, 1)
settings["irc"]["port"] = int(settings["irc"]["port"])
settings["irc"]["nick_length_limit"] = int(settings["irc"]["nick_length_limit"])
