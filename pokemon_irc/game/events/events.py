from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from string import ascii_letters, digits
from random import SystemRandom
from itertools import count
from pokemon_irc.exceptions.event import EventError
import hashlib
import logging
from .utils import get_player, get_pokemon
from datetime import datetime

random = SystemRandom()
choice = random.choice

progression_model = {
    'medium_fast': [(n**3) for n in range(101)],
}


def create_player(player_name, password):
    player = get_player(player_name, exc=False)
    if player:
        raise EventError("alreadyreg", name=player_name)

    if len(password) < 5:
        raise EventError("shortpass", length=5)

    letters = ascii_letters + digits
    salt = ''.join(choice(letters) for _ in range(25))
    hashed_password = hashlib.md5((salt+password).encode('utf-8')).hexdigest()

    new_player = orm.Player(
        name=player_name,
        salt=salt,
        password=hashed_password,
    )

    session.add(new_player)
    session.commit()
    return True


def authorize_player(player_name, password):
    player = get_player(player_name)
    correct_password = player.password

    password = hashlib.md5(
        (player.salt + password).encode('utf-8')
    ).hexdigest()

    if password != correct_password:
        raise EventError('badpassword')
    else:
        return player


def rename_pokemon(player_name, pokemon_name, new_pokemon_name):
    pokemon = get_pokemon(player_name, pokemon_name)
    new_pokemon = get_pokemon(player_name, new_pokemon_name, exc=False)
    if new_pokemon:
        raise EventError('alreadypokemon', name=new_pokemon_name)
    pokemon.name = pokemon_name
    session.commit()


def create_pokemon(player_name, pokemon_name):
    name = pokemon_name.capitalize()
    player = get_player(player_name)

    p = session.query(orm.Pokemon).filter_by(name=name).first()
    if not p:
        raise EventError('nopokemon', name=player_name, pokename=pokemon_name)
    used_names = (x.name for x in player.pokemons)

    if pokemon_name in used_names:

        for i in (str(i) for i in count(2)):
            if not (pokemon_name + i) in used_names:
                pokemon_name = pokemon_name + i
                break

    pp = orm.PlayerPokemon(
        name=pokemon_name,
        player_id=player.id,
        base_pokemon_id=p.id,
        hp=p.hp,
        current_hp=p.hp,
        attack=p.attack,
        defence=p.defence,
        special_attack=p.special_attack,
        special_defence=p.special_defence,
        speed=p.speed,
    )
    session.add(pp)
    session.commit()


def del_pokemon(pokemon_id):
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()

    session.delete(pokemon)
    session.commit()


def summon_pokemon(battle, owner, pokemon_name):
    pokemon = get_pokemon(pokemon_name)
    pass


def recall_pokemon(battle, pokemon_name):
    pass


def list_moves(player_name, pokemon_name):
    pokemon = get_pokemon(player_name, pokemon_name)

    yield from (move.name for move in pokemon.known_moves)


def challenge_player(player1_name, player2_name):
    player1 = get_player(player1_name)
    player2 = get_player(player2_name)
    battle = orm.Battle(
        challenger=player1,
        challengee=player2,
        date=datetime.now()
    )
    session.add(battle)
    session.commit()
    return battle.id


def list_pokemons(player_name):
    player = get_player(player_name)
    pokemons = player.pokemons
    yield from (pokemon_details.format(p=p) for p in pokemons)


def level_up(pokemon, new_level):
    pokemon_id = pokemon.base_pokemon.id
    moves = session.query(orm.PokemonMoveLevel).\
        filter(
            orm.PokemonMoveLevel.id == pokemon_id,
            orm.PokemonMoveLevel.level.between(old_level, new_level)
        )


def cast_move(a_pokemon, d_pokemon, move):
    orm.session(orm.Move).filter
