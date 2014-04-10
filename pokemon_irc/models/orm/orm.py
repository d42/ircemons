#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String,\
    ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from settings import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI)


class PokemonType(Base):
    __tablename__ = "pokemon_type"
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))
    type_id = Column(Integer, ForeignKey('type.id'))


class PokemonMove(Base):
    __tablename__ = "pokemon_move"
    id = Column(Integer, primary_key=True)
    level = Column(Integer, nullable=False)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))
    move_id = Column(Integer, ForeignKey('move.id'))


class KnownMove(Base):
    __tablename__ = "known_move"
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('player_pokemon.id'))
    move_id = Column(Integer, ForeignKey('move.id'))


class DefaultColumns:
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


    def __str__(self):
        return "%s" % self.name


class Pokemon(Base, DefaultColumns):
    __tablename__ = 'pokemon'
    types = relationship("Type", secondary="pokemon_type")
    moves = relationship("Move", secondary="pokemon_move")
    player_pokemons = relationship("PlayerPokemon", backref="base_pokemon")
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defence = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defence = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)


class Type(Base, DefaultColumns):
    __tablename__ = 'type'


class DamageTypesRelation(Base):
    __tablename__ = 'damage_types_relation'
    id = Column(Integer, primary_key=True)
    attack = Column(Integer, ForeignKey("type.id"))
    defence = Column(Integer, ForeignKey("type.id"))
    # attack = relationship('Type')
    # defence = relationship('Type')
    dmg_mult = Column(Float, nullable=False)


class MoveCategory(Base, DefaultColumns):
    __tablename__ = 'move_category'


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


class Effect(Base):
    __tablename__ = 'effect'
    id = Column(Integer, primary_key=True)
    description = Column(String(150), unique=True)


class PlayerPokemon(Base):
    __tablename__ = "player_pokemon"
    id = Column(Integer, primary_key=True)
    base_pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    name = Column(String(50))
    xp = Column(Integer, default=0)
    level = Column(Integer, default=0) # do i need those separate ,_<
    player_id = Column(Integer, ForeignKey('player.id'))
    known_moves = relationship("Move", secondary="known_move")
    hp = Column(Integer, nullable=False)
    current_hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defence = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defence = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)


class Player(Base, DefaultColumns):
    __tablename__ = "player"
    pokemons = relationship("PlayerPokemon", backref="player")





Base.metadata.create_all(engine)
