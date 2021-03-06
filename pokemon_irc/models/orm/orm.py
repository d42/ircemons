#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String,\
    ForeignKey, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pokemon_irc.settings import settings

Base = declarative_base()
engine = create_engine(settings["game"]["database_uri"])

class DefaultColumns:
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


    def __str__(self):
        return "%s" % self.name


#                   This stuff stouldn't change during the game
###############################################################################
###############################################################################
###############################################################################

class PokemonType(Base):
    """ many to many, between Pokemon and Type, had to be done """
    __tablename__ = "pokemon_type"
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    type_id = Column(Integer, ForeignKey("type.id"))


class PokemonMoveLevel(Base):
    """ pokemon's move learn level """
    __tablename__ = "pokemon_move_level"
    id = Column(Integer, primary_key=True)

    move_id = Column(Integer, ForeignKey("move.id"))
    pokemon_id = Column(Integer, ForeignKey("pokemon.id"))
    pokemon = relationship("Pokemon", backref="move_level")
    move = relationship("Move")

    level = Column(Integer)


class Pokemon(Base, DefaultColumns):
    __tablename__ = "pokemon"
    types = relationship("Type", secondary="pokemon_type")
    moves_levels = relationship("Move", secondary="pokemon_move_level")
    player_pokemons = relationship("PlayerPokemon", backref="base_pokemon")

    evolution_level = Column(Integer)
    evolves_to_id = Column(Integer, ForeignKey("pokemon.id"))

    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defence = Column(Integer, nullable=False)
    special_attack = Column(Integer, nullable=False)
    special_defence = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)


class Type(Base, DefaultColumns):
    __tablename__ = "type"


class TypesRelation(Base):
    __tablename__ = "types_relation"
    id = Column(Integer, primary_key=True)
    attack_id = Column(Integer, ForeignKey("type.id"))
    attack = relationship("Type", foreign_keys=[attack_id])
    defence_id = Column(Integer, ForeignKey("type.id"))
    defence = relationship("Type", foreign_keys=[defence_id])
    dmg_mult = Column(Float, nullable=False)


class Ability(Base, DefaultColumns):
    """ """
    __tablename__ = "ability"


###############################################################################
class Category(Base, DefaultColumns):
    """ Each move is either special, physical or stat
        Physical uses attack/defence stats while special
        uses special_{attack,defence}
    """
    __tablename__ = "category"


class Move(Base, DefaultColumns):
    __tablename__ = "move"
    effect = relationship("Effect")

    type_id = Column(Integer, ForeignKey("type.id"))
    effect_id = Column(Integer, ForeignKey("effect.id"))
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    type = relationship("Type")
    category = relationship("Category")

    power = Column(Integer, nullable=False)
    accuracy = Column(Integer, nullable=False)
    pp = Column(Integer, nullable=False)

    effect_prob = Column(Integer)

    def __repr__(self):
        return self.name


class Effect(Base):
    __tablename__ = "effect"
    id = Column(Integer, primary_key=True)
    description = Column(String(150), unique=True)

    def __str__(self):
        return self.description

###############################################################################
################  dynamic game entries ########################################
###############################################################################


class KnownMove(Base):
    """ move currently know by a player's pokemon """
    __tablename__ = "known_move"
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey("player_pokemon.id"))
    move_id = Column(Integer, ForeignKey("move.id"))
    pokemon = relationship("PlayerPokemon")
    move = relationship("Move")
    pp = Column(Integer)


class PlayerPokemon(Base):
    __tablename__ = "player_pokemon"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    base_pokemon_id = Column(Integer, ForeignKey("pokemon.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("player.id"))

    xp = Column(Integer, default=0)
    level = Column(Integer, default=1) # do i need those separate ,_<
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
    password = Column(String(16), nullable=False)  # TODO: different hashes and stuff
    salt = Column(String(25), nullable=False)
    matches_won = Column(Integer, default=0, nullable=False)
    matches_total = Column(Integer, default=0, nullable=False)
    xp_total = Column(Integer, default=0, nullable=False)



#class BattleMove(Base):
    #__tablename__ = "battle_move"
    #id = Column(Integer, primary_key=True)

    #battle_id = Column(ForeignKey("battle.id"))
    #battle = relationship("Battle") yadda, yadda. I'll add it later ;3


class BattlePokemon(Base): # Mostly to keep the evasion stat
    __tablename__ = "battle_pokemon"
    id = Column(Integer, primary_key=True)
    battle_id = Column(ForeignKey("battle.id"))
    pokemon_id = Column(ForeignKey("player_pokemon.id"))

    battle = relationship("Battle")
    pokemon = relationship("PlayerPokemon")
    evasion = Column(Float, nullable=False)


class Battle(Base):
    __tablename__ = "battle"
    id = Column(Integer, primary_key=True)
    challenger_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    challengee_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("player.id"), nullable=True)
    pokemons = relationship("BattlePokemon")
    challengee = relationship("Player", foreign_keys=[challengee_id])
    challenger = relationship("Player", foreign_keys=[challenger_id])
    winner = relationship("Player", foreign_keys=[winner_id])
    date = Column(DateTime)



#Base.metadata.create_all(engine) # bad for testing ;3
