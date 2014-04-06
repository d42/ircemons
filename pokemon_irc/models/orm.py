#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String,\
    ForeignKey, Float, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI)


class DefaultColumns:
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Pokemon(Base, DefaultColumns):
    __tablename__ = 'pokemon'
    type = Column(Integer, ForeignKey("type.id"))
    hp = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    special_attack = Column(Integer)
    special_defence = Column(Integer)
    speed = Column(Integer)


class Type(Base, DefaultColumns):
    __tablename__ = 'type'


class DamageTypesRelation(Base):
    __tablename__ = 'damage_types_relation'
    id = Column(Integer, primary_key=True)
    type_a = Column(Integer, ForeignKey("pokemon.id"))
    type_b = Column(Integer, ForeignKey("pokemon.id"))
    dmg_to_a = Column(Float)
    dmg_to_b = Column(Float)


class MoveCategory(Base, DefaultColumns):
    __tablename__ = 'move_category'
    id = Column(Integer, primary_key=True)


class Move(Base, DefaultColumns):
    __tablename__ = 'move'
    type = Column(Integer, ForeignKey("type.id"))
    category = Column(Integer, ForeignKey("move_category.id"))
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)
    effect = Column(Integer, ForeignKey("effect.id"))


class Ability(Base, DefaultColumns):
    __tablename__ = 'ability'


class Effect(Base, DefaultColumns):
    __tablename__ = 'effect'
    description = Column(String)

Base.metadata.create_all(engine)
