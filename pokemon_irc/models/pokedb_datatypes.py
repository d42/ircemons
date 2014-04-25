#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from collections import namedtuple, UserList
from pokemon_irc.settings import settings
pokedb_settings = settings["pokedb"]

from pokemon_irc.web import PokeDBMachine, INF, MINUS
from pokemon_irc.models import orm
import logging

poke_machine = PokeDBMachine()

class cache(object):
    def __init__(self, method, name=None):
        self.method = method
        self.name = name or method.__name__
        self.__doc__ = method.__doc__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        result = self.method(inst)
        setattr(inst, self.name, result)
        return result


class Base:
    classes = "data-table wide-table"  # Css classes on the website
    xpath = "//table[@class='{}'][1]/tbody/tr"
    key_slots = ('name',)
    models = {}
    model_handlers = {}
    getter = poke_machine.poke_get


    def __init__(self):

        self.xpath = self.xpath.format(self.classes)
        self.defaults, self.names = zip(*self.slots)
        self.model_handlers[self.__tablename__] = self
        self.models[self.__tablename__] = {}

    def __call__(self, *values):
        assert len(self.slots) == len(values)
        return self.namedtuple(*values)

    @cache
    def _namedtuple(self):
        return namedtuple(self.__tablename__, self.names)

    def namedtuple(self, *args):
        args = tuple(a.lower() if type(a) == str else a for a in args)
        return self._namedtuple(*args);


    def all(self):
        yield from self.getter(self)

    def gen_key(self, t):
            key = tuple(getattr(t, x) for x in self.key_slots)
            if len(key) == 1:
                key = key[0]
            return key

    def sync_db(self):

        logging.debug("syncing %s", self.__tablename__)
        models = self.models[self.__tablename__]
        for t in self.all():

            key = self.gen_key(t)
            if not all(key) or key in models: continue

            submodels = []
            if hasattr(self, 'sub'):
                for table, e_desc in self.sub:
                    handler = self.model_handlers[table]
                    sub_e = [getattr(t, d) for d in e_desc]     # so many single letters ;_;

                    if not all(sub_e):
                        submodels.append(None)

                    else:
                        submodels.append(
                            handler.add_model(handler.namedtuple(*sub_e))
                        )

            m = self.model(t, *submodels)
            assert m
            models[key] = m

            orm.session.add(m)
        orm.session.commit()

    def add_model(self, t):
        key = self.gen_key(t)

        if self.gen_key(t) not in self.models[self.__tablename__]:
            m = self.model(t)
            orm.session.add(m)
            self.models[self.__tablename__][key] = m
            #orm.session.commit()

        return self.models[self.__tablename__][key]

    def get_model(self, model_group, model_name):
        if model_group not in self.models:
            handler = self.model_handlers[model_group]
            handler.sync_db()

        value = self.models[model_group][model_name]
        return value


def list_lower(x):
    return [e.lower() for e in x]


class Pokemon(Base):
    __tablename__ = "pokemon"
    url = pokedb_settings["pokemons"]
    xpath = "//table[@id='pokedex']/tbody/tr"
    slots = (
        (int, 'id'),
        (str, 'name'),
        (list_lower, 'types'),
        (int, 'total'),
        (int, 'hp'),
        (int, 'attack'),
        (int, 'defence'),
        (int, 'special_attack'),
        (int, 'special_defence'),
        (int, 'speed')
    )

    def model(self, t):
        m = orm.Pokemon()
        m.id = t.id
        m.name = t.name
        m.types = [self.get_model('type', x) for x in t.types]
        m.hp = t.hp
        m.attack = t.attack
        m.defence = t.defence
        m.special_attack = t.special_attack
        m.special_defence = t.special_defence
        m.speed = t.speed
        return m


class Move(Base):
    __tablename__ = "move"
    url = pokedb_settings["moves"]
    xpath = '//table[@id="moves"]/tbody/tr'
    slots = (
        (str, 'name'),
        (str, 'type'),
        (str, 'category'),
        (int, 'power'),
        (int, 'accuracy'),
        (int, 'pp'),
        (str, 'tm'),
        (str, 'effect'),
        (int, 'effect_prob')
    )
    sub = (
        ('category', ('category',)),
        ('effect', ('effect',)),
    )

    def model(self, t, category, effect):
        m = orm.Move()
        m.name = t.name
        m.effect = effect
        m.type = self.get_model('type', t.type)
        m.category = category
        m.power = t.power
        m.accuracy = t.accuracy
        m.pp = t.pp
        m.effect_prob = t.effect_prob
        return m


class Ability(Base):
    __tablename__ = "ability"
    slots = (
        (str, 'name'),
        (int, 'pokemon'),
        (str, 'description'),
        (int, 'gen')
    )

    def model(self, t):
        m = orm.Ability()
        return m


class MoveLevel(Base):
    __tablename__ = "move_level"
    xpath = "//li[@id='svtabs_moves_13']//table[1]/tbody/tr"
    url = pokedb_settings["pokemon"]
    slots = (
        (int, 'level'),
        (str, 'name'),
    )


class Category(Base):
    __tablename__ = "category"
    url = pokedb_settings["moves"]
    xpath = '//table[@id="moves"]/tbody/tr/td[3]'
    slots = (
        (str, 'name'),
    )

    def model(self, t):
        m = orm.Category(name=t.name)
        return m


class Effect(Base):
    __tablename__ = "effect"
    url = pokedb_settings["moves"]
    xpath = '//table[@id="moves"]/tbody/tr/td[8]'
    key_slots = ('description', )
    slots = (
        (str, 'description'),
    )

    def model(self, t):
        print(t)
        m = orm.Effect(description=t.description)
        return m


class DamageType(Base):
    __tablename__ = "damage_type"
    url = pokedb_settings["types"]
    xpath = '//table[@class="type-table"]/tbody/tr'
    getter = poke_machine.poke_get_type_damage
    key_slots = ('attack', 'defence')
    slots = (
        (str, 'attack',),
        (str, 'defence',),
        (float, 'dmg_mult',)
    )

    sub = (
        ('type', ('attack',)),
        ('type', ('defence',)),
    )

    def model(self, t, attack, defence):
        m = orm.TypesRelation()
        m.attack = attack
        m.defence = defence
        m.dmg_mult = t.dmg_mult
        return m


class Type(Base):
    __tablename__ = 'type'
    slots = (
        (str.lower, 'name'),
    )

    def all(self):
        return (self.namedtuple(x) for x in (
            'normal', 'fire', 'water', 'electric', 'grass',
            'ice', 'fighting', 'poison', 'ground', 'flying',
            'psychic', 'bug', 'rock', 'ghost', 'dragon',
            'dark', 'steel', 'fairy')
        )

    def model(self, t):
        return orm.Type(name=t.name)


category = Category()


def do_stuff():
    t = Type()
    p = Pokemon()
    m = Move()
    ml = MoveLevel()
    dt = DamageType()
    e = Effect()
    for derp in [dt]:
        derp.sync_db()
