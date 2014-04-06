#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String,\
    ForeignKey, Float, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI)


class Pokemon(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(ForeignKey)
    hp = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    special_attack = Column(Integer)
    special_defence = Column(Integer)
    speed = Column(Integer)


class DamageType(Base):
    name = Column(String)


class DamageTypesRelation(Base):
    type_a = Column(ForeignKey)
    type_b = Column(ForeignKey)
    dmg_to_a = Column(Float)
    dmg_to_b = Column(Float)


class Move(Base):
    name = Column(String)
    type = Column(ForeignKey)
    category = Column(ForeignKey)
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)

    effect = Column(ForeignKey)


class Effect(Base):
    description = Column(String)

    
