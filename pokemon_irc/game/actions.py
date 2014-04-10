from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from pokemon_irc.game import events
from collections import deque
import logging


class GMActions:

    current_matches = {}

    def __init__(self, GMBot):
        self.main_actions = {
            'register': self._register_player,
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

        self.gm = GMBot


    def query_run(self, nickserv_auth, command_tokens):
        command_tokens = deque(command_tokens)

        state = self.query_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)
        return "something went wrong"

    def admin_run(self, command_tokens):
        state = self.admin_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)
        return False

    def battle_run(self, nickserv_auth, command_tokens):
        state = self.battle_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)
        return "something went wrong"

    def main_channel_run(self, nickserv_auth, command_tokens):
        command_tokens = deque(command_tokens)

        state = self.main_actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)
        return "something went wrong"

    def _list_pokemons(self, player_name):
        return events.list_pokemons(player_name)

    def _register_player(self, player_name):
        return events.create_player(player_name)

    def _print(self, *message, player_name):
        return ' '.join(message)

    def _challenge_player(self, challengee, player_name):
        pass

    def _recall_pokemon(name, player_name, battle):
        pass

    def _summon_pokemon(name, player_name, battle):
        pass

    def _accept_challenge(self, challengee, player_name):
        pass

    def _yield_match(self, challengee, player_name):
        pass

    def _display_help(self, player_name):
        pass


class PokemonActions:
    pass
