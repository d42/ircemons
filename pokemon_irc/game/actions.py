from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from pokemon_irc.game import events
from collections import deque
import logging


class GMActions:


    def __init__(self, GMBot):
        self.public_actions = {
            'register': self._register_player,
            'auth': self._auth_player,
        }

        self.main_actions = {
            'challenge': self._challenge_player,
            'accept': self._accept_challenge,
            'yield': self._yield_match,
            'help': self._display_help,
        }

        self.battle_actions = {
            'recall': self._recall_pokemon,
            'summmon': self._summon_pokemon
        }

        self.admin_actions = {
            'print': self._print
        }

        self.query_actions = {
            'list': {'pokemons': self._list_pokemons}
        }
        self.query_actions.update(self.main_actions)
        self.main_actions.update(self.public_actions)

        self.gm = GMBot

    def key_error_decorator(func):
        def inner(*args):
            try:
                return func(*args)
            except KeyError:
                return "No such command"
            except TypeError as e:
                return str(e)
        return inner

    @key_error_decorator
    def query_run(self, user, command_tokens):
        command_tokens = deque(command_tokens)

        state = self.query_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, user=user)
        return "something went wrong"

    @key_error_decorator
    def admin_run(self, command_tokens):
        state = self.admin_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)
        return False

    @key_error_decorator
    def battle_run(self, user, command_tokens):
        state = self.battle_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, user=user)
        return "something went wrong"

    @key_error_decorator
    def main_channel_run(self, user, command_tokens):
        command_tokens = deque(command_tokens)

        state = self.main_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, user=user)
        return "something went wrong"

    def _list_pokemons(self, user):
        return events.list_pokemons(user.auth)

    def _register_player(self, password, user):
        return events.create_player(user.nick, password)

    def _auth_player(self, password, user):
        return events.authorize_player(user.nick, password)


    def _print(self, *message, user):
        return ' '.join(message)

    def _challenge_player(self, challengee, user):
        if not self.gm.player_on_main_channel(challengee): return "You can't challenge someone who's not on the channel."



        self.gm.write(challengee, "{} has challened you to a battle".format(user))

        return "{} has been challenged".format(challengee)

    def _recall_pokemon(name, user, battle):
        pass

    def _summon_pokemon(name, user, battle):
        pass

    def _accept_challenge(self, challenger=None, user=None):
        if not user: return "something went wrong"

        pb = self.gm.pending_battles[user]
        if not challenger:
            if len(pb) != 1:
                return "there's more than one request, specify player"
            request = pb.popitem()
            request.accept()
            
        pass

    def _yield_match(self, challengee, user):
        pass

    def _display_help(self, user):
        pass


class PokemonActions:
    pass
