from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from string import ascii_letters, digits
from random import SystemRandom
import hashlib
import logging

random = SystemRandom()
choice = random.choice

progression_model = {
    'medium_fast': [(n**3) for n in range(101)],
}


def check_level(pokemon, progression_type='medium_fast'): # TODO: kind of poor ,_,
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


def create_player(player_name, password):
    q = session.query(orm.Player).filter_by(name=player_name).first()
    if q: return "already registered"

    if len(password) < 5: return "dude..."

    letters = ascii_letters + digits
    salt = ''.join(choice(letters) for _ in range(25))
    hashed_password = hashlib.md5( (salt+password).encode('utf-8') ).hexdigest()
    session.add(orm.Player(name=player_name, salt=salt, password=hashed_password))
    session.commit()
    return "registered successfully"


def authorize_player(player_name, password):
    q = session.query(orm.Player).filter_by(name=player_name).first()
    if not q: return "not registerd"

    if hashlib.md5((q.salt + password).encode('utf-8')).hexdigest() == q.password:
        return "authorized successfully"

    return "wrong password"



def create_pokemon(player_name, pokemon_name):
    name = pokemon_name.capitalize()
    q = session.query(orm.Player).filter_by(name=player_name).first()
    p = session.query(orm.Pokemon).filter_by(name=name).first()
    if not q: return "No such player"
    if not p: return "no such pokemon"

    session.query()
    pp = orm.PlayerPokemon(
        name=("{}'s {}".format(q.name, p.name)),
        player_id=q.id,
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

    return "created sucessfully"


def del_pokemon(pokemon_id):
    pokemon = session.query(orm.PlayerPokemon).filter_by(id=pokemon_id).first()
    pokemon_name = pokemon.name

    session.delete(pokemon)
    session.commit()

    return "{} dies".format(pokemon_name)


def list_pokemons(player_name):
    player = session.query(orm.Player).filter_by(name=player_name).first()
    pokemons = player.pokemons
    template = (
        "[{p.base_pokemon}|{p.name}], [hp:{p.current_hp}/{p.hp}, att:{p.attack}, "
        "def:{p.defence}, sp att:{p.special_attack}, sp def:{p.special_defence}, "
        "speed:{p.speed}, level:{p.level}] {p.known_moves}"
    )
    return "\n".join(template.format(p=p) for p in pokemons)
