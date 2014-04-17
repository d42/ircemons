import irc.bot
import irc.strings
import logging
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from pokemon_irc.settings import settings
from pokemon_irc.text import TextManager
from .actions import GMActions
from collections import deque, defaultdict, namedtuple
tm = TextManager("action_responses")
irc_settings = settings['irc']

user = namedtuple("user", ["name", "real_name", "hostname"])
user_auth = namedtuple("auth", ["hostname", "player"])


class BotBase(irc.bot.SingleServerIRCBot):
    def __init__(self, server_list, nickname, realname):
        super().__init__(server_list, nickname, realname)
        self.connection.buffer_class.errors = 'replace'

    def parse_source(self, source):
        # Shame there's no documentation for it and

        u = user(
            name=source.nick,
            real_name=source.user,
            hostname=source.host
        )
        return u

    def ircify(self, nickname):
        """ turn into valid irc nickname """
        pass

    def tokenize_command(self, message, name=None, query=False):
        if not name: name = self.name
        command = None

        if message.startswith(name+':'):
            command = message[len(name)+1:].strip()
        elif query:
            command = message.strip()

        if command:
            logging.debug(command)
            tokens = deque(command.split())
            return tokens
        return False

    def write(self, channel, message):
        """ send message to a channel(username) """
        for line in message.split('\n'):
            print("#%s %s: %s" % (channel, irc_settings['gm_nick'], line))
            self.connection.privmsg(channel, line)

    def respond(self, nick, channel, message):
        """ send message to a channel, prefixed with nick: """
        print("#%s %s: %s" % (channel, nick, message))
        self.connection.privmsg(channel, "%s: %s" % (nick, message))


class PokemonBot(BotBase):
    def __init__(self, pokemon, channel, nickname, owner, server=irc_settings['server'], port=irc_settings['port']):

        self.name = nickname
        realname = pokemon.base_pokemon.name
        self.channel = channel
        self.owner = owner
        super().__init__([(server, port)], nickname, realname)

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        user = self.parse_source(e.source)
        if user == self.owner:
            self.write(self.channel, "kekekeke")
        else:
            import ipdb; ipdb.set_trace()

    def on_pubmsg(self, c, e):
        user = self.parse_source(e.source)
        pass


class GMBot(BotBase):
    authorized = {}
    pending_battles = defaultdict(dict)
    current_battles = defaultdict(dict)
    b = False

    def __init__(
        self,
        channel=irc_settings["main_channel"],
        nickname=irc_settings["gm_nick"],
        realname=irc_settings["realname"],
        server=irc_settings["server"],
        port=irc_settings["port"],
        bot_list=None
        ):

            self.name = nickname

            self.bot_list = bot_list

            super().__init__([(server, port)], nickname, realname)
            self.channel = channel
            self.actions = GMActions(self)

            self.connection.add_global_handler("part", self.on_exit, -42)
            self.connection.add_global_handler("quit", self.on_exit, -42)
            self.connection.add_global_handler("nick", self.move_auth, -42)
            self.connection.add_global_handler("welcome", self.clear_auth, 1)

    # ##### SUCH AUTH ######

    def clear_auth(self, c, e):
        self.authorized = {}

    def get_auth(self, user):
        if user.name not in self.authorized:
            return False

        if user.hostname == self.authorized[user.name]:
            return self.authorized[user.name]

    def move_auth(self, c, e):
        user = self.parse_source(e.source)
        player = self.get_auth(user)

        if player:
            self.authorized[e.target] = player
            del self.authorized[user.name]

    def auth(self, user, player):
        logging.debug(user, "authorized")
        self.gm.authorized[user.name] = user_auth(user.hostname, player)

    def deauth(self, user):
        logging.debug(user, "deauthorized")
        auth = self.get_auth(user)
        if not auth:
            return

        del self.authorized[user.name]

    ####### VERY AUTH ######

    ####### SUCH IRC EVENTS ######

    def on_join(self, c, e):
        channel = e.target
        user = self.parse_source(e.source)

        battle = self.current_battles.get(channel, None)
        if not battle: return

        if user.name == c.get_nickname():
            c.invite(battle["player1"], channel)
            c.invite(battle["player2"], channel)
            c.topic(battle["channel"], new_topic="herp derp")
        else:
            if user.name in (battle["player1"], battle["player2"]):
                self.respond(user.name, channel, "jp2gmd")

    def on_exit(self, c, e):
        user = self.parse_source(e.source)

        if e.type == "quit":
            self.deauth(user)

        elif e.target == irc_settings['main_channel']:  # parts from main channel
            self.deauth(user)

    def on_nicknameinuse(self, c, e):
        raise Exception("get me a real name!")

    def on_welcome(self, c, e):
        c.join(self.channel)

    # TODO: refactoring this with on_pubmsg would be cool
    def on_privmsg(self, c, e):

        user = self.parse_source(e.source)
        tokens = self.tokenize_command(e.arguments[0], query=True)

        if not tokens:
            return

        player = self.get_auth(user)

        if player and tokens[0] in self.actions.no_auth_actions:
            self.write(user.name, tm.get("alreadyauth"))
            return

        if not player and tokens[0] not in self.actions.public_actions:
            self.write(user.name, tm.get("noauth"))
            return

        ok, message = self.actions.query_run(user, tokens)
        self.write(user.name, message)

    def on_pubmsg(self, c, e):
        user = self.parse_source(e.source)
        tokens = self.tokenize_command(e.arguments[0])

        if not tokens:
            return

        player = self.get_auth(user)

        if player and tokens[0] in self.actions.no_auth_actions:
            self.respond(user.name, e.target, "already authorized")
            return

        if not player and tokens[0] not in self.actions.public_actions:
            self.respond(user.name, e.target, "not authorized")
            return

        if e.target == irc_settings["main_channel"]:
            ok, message = self.actions.main_channel_run(user, tokens)
        else:
            battle = self.current_battles[e.target]

            if user.name not in (battle["player1"], battle["player2"]):
                self.respond(user.name, e.target, tm.get("notyourbattle"))
                return

            if user.name not in battle["current_player"]:
                self.respond(user.name, e.target, tm.get("notyourturn"))
                return

            ok, message = self.actions.battle_run(battle, user, tokens)

            if ok:
                self.change_current_player(battle)

        self.respond(user.name, e.target, message)

    def change_current_player(self, battle):
        if battle["current_player"] == battle["player1"]:
            battle["current_player"] = battle["player2"]
        else:
            battle["current_player"] = battle["player1"]

    # ###### VERY IRC EVENTS ######
    def _run(self, command, channel=None):
        # pointless, probably bad, but i found it interesting

        user = user(name="admin", hostname="127.0.0.1", realname="admin")
        tokens = deque(command.split())
        if not channel:
            message = self.actions.admin_run(user, tokens)

        elif channel == irc_settings["main_channel"]:
            message = self.actions.main_channel_run(name, tokens)

        else:
            message = self.actions.battle_run(name, tokens)

        self.write(channel, message)

    def summon_pokemon(self, user, battle, pokemon):
        """ Deploys a PokeBot on IRC"""

        player = pokemon.player

        if battle["pokemon"][player.name]:
            self.write(battle["channel"], tm.get("alreadypokemon"))
        id = pokemon.id

        logging.debug("{name} deploys {pokename} in {battlename}".format(
            name=player.name,
            pokename=pokemon.name,
            battlename=battle['channel']
        ))

        p = PokemonBot(
            pokemon,
            channel=battle["channel"],
            nickname="%s[%s]" % (pokemon.name, player.name),
            owner=user
        )
        p.gm = self
        battle["pokemon"][player.name] = p
        p._connect()
        self.bot_list[id] = p
    def recall_pokemon(self, user, battle):

        pokemon = battle["pokemon"][player.name]
        if not pokemon:
            self.respond()

    def start_battle(self, challenger, challengee):
        #  TODO: are there any invalid characters
        channel = "###" + challenger + "_vs_" + challengee

        # battle = battle(challenger, challengee, channel)
        battle = {
            "player1": challenger,
            "player2": challengee,
            "channel": channel,
            "current_player": challengee,
            "pokemon": {
                challenger: None,
                challengee: None
            }
            }

        if channel not in self.current_battles:
            self.current_battles[channel] = battle

        self.connection.join(channel)

    def player_on_main(self, player_name):
        if player_name in self.channels[irc_settings["main_channel"]].userdict:
            return True
