#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from pokemon_irc.exceptions.event import EventError


def get_player(player_name, exc=True):
    player = session.query(orm.Player).filter_by(name=player_name).first()
    if not player and exc:
        raise EventError('nouser', name=player_name)
    return player


def get_pokemon(player_name, pokemon_name, exc=True):
    player = get_player(player_name)
    if not player and exc:
        raise EventError('nouser', name=player_name)
    pokemon = session.query(orm.PlayerPokemon).filter_by(
        name=pokemon_name,
        player=player).first()

    if not pokemon:
        raise EventError('nopokemon', name=player_name, pokename=pokemon_name)
    return pokemon


def check_level(pokemon, progression_type='medium_fast'):  # TODO: kind of poor ,_,
    model = progression_model[progression_type]
    level = pokemon.level
    xp = pokemon.xp
    required_xp = model[level]
    if xp >= required_xp:
        return True
    return False


def add_xp(pokemon_id, xp):
    leveled_up = False
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    level = pokemon.level
    pokemon.xp += xp
    while check_level(pokemon):
        if level == 100: break
        logging.debug("%s levels up to %s" % (pokemon.name, pokemon.level+1))
        pokemon.level += 1

    session.commit()
    return pokemon.level, pokemon.xp

