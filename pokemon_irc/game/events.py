from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
import logging


progression_model = {
    'medium_fast': [(n**3) for n in range(101)],
}


def check_level(pokemon, progression_type='medium_fast'): # TODO: kind of poor ,_,
    model = progression_model[progression_type]
    level = pokemon.level
    xp = pokemon.xp
    required_xp = model[level]
    if xp >= required_xp:
        import ipdb; ipdb.set_trace()
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

