from pokemon_irc.models import orm
from pokemon_irc.models.orm import session
from collections import deque
import logging






class GMActions:

    current_matches = {}


    def __init__(self, GMBot):
        self.actions = {
            'register': self._register_player,
            'challenge': self._challenge_player,
            'accept': self._accept_challenge,
            'yield': self._yield_match,
            'help': self._display_help
        }

        self.gm = GMBot


    #@error_handler
    def run(self, nickserv_auth, command_tokens):
        command_tokens = deque(command_tokens)

        state = self.actions
        while command_tokens:
            state = state[command_tokens.popleft()]
            if hasattr(state, '__call__'):
                return state(*command_tokens, player_name=nickserv_auth)

    def _register_player(self, player_name):
        return "kek"
        pass

    def _challenge_player(self, challengee, player_name):
        pass

    def _accept_challenge(self, challengee, player_name):
        pass

    def _yield_match(self, challengee, player_name):
        pass

    def _display_help(self, player_name):
        pass


class PokemonActions:
    pass

