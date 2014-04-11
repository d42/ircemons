import irc.bot
import irc.strings
import logging
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from pokemon_irc.settings import IRC_SERVER, IRC_PORT, IRC_MAIN_CHANNEL, IRC_GM_NICK, IRC_REALNAME, IRC_OWNER
from pokemon_irc.game.actions import GMActions
from collections import deque, defaultdict, namedtuple

user = namedtuple('user', ['nick', 'real_name', 'hostname'])


class Authorization:

    def check_auth(self, user_name):
        return user_name



# handle 330

class PokeBot(irc.bot.SingleServerIRCBot):
    auth = Authorization()

    def parse_source(self, source):
        t = str.maketrans('!@', '  ')
        u = user(*source.translate(t).split())
        logging.debug(u)
        return u

    def ircify(self, nickname):
        """ turn into valid irc nickname """
        pass

    def parse_command(self, message, name=None):
        if not name: name = self.name

        if message.startswith(self.name+':'):
            command = message[len(self.name)+1:].strip()
            logging.debug(command)
            tokens = deque(command.split())

            return tokens
        return False
    

class PokemonBot(PokeBot):
    def __init__(self, pokemon, battle, server=IRC_SERVER, port=IRC_PORT):

        self.name = self.ircify(pokemon.name)
        realname = pokemon.base_pokemon.name
        self.channel = ircify(battle.name)
    
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], self.name, realname)


        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        nick = self.nick(e.source)
        print(nick)
        self.connection.privmsg('nickserv', 'info %s' % nick)
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        pass
        #a = e.arguments[0].split(":", 1)
        #if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            #self.do_command(e, a[1].strip())
        #return

    #def do_command(self, e, cmd):
        #nick = e.source.nick
        #c = self.connection



class GMBot(PokeBot):
    auth_queue = deque()
    authorized = {}
    pending_battles = defaultdict(dict)
    current_battles = defaultdict(dict)

    def __init__(
        self,
        channel=IRC_MAIN_CHANNEL,
        nickname=IRC_GM_NICK,
        realname=IRC_REALNAME,
        server=IRC_SERVER,
        port=6667):

        self.name = nickname

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, realname)
        self.channel = channel
        self.actions = GMActions(self)

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privnotice(self, c, e):
        print(e.arguments)


    def on_privmsg(self, c, e):
        nick = get_nick(e.source)
        tokens = deque(e.arguments[0].split())
        nickserv_auth = self.auth.check_auth(nick)

        if not nickserv_auth:
            self.respond(nick, e.target, "auth to nickserv plx")
            return
        message = self.actions.query_run(nickserv_auth, tokens)

        self.write(nick, message)


    def player_on_main_channel(self, nick):
        return nick in self.channels[IRC_MAIN_CHANNEL].users()


    def on_pubmsg(self, c, e):
        user = self.parse_source(e.source)
        tokens = self.parse_command(e.arguments[0])

        if not tokens: return

        player = self.authorized.get((user.nick, user.hostname), False)

        if player:
            user.auth = player

        if not player and tokens[0] not in self.actions.public_actions:
            self.respond(user.nick, e.target, "not authorized")
            return

        if e.target == IRC_MAIN_CHANNEL:
            message = self.actions.main_channel_run(user, tokens)
        else:
            message = self.actions.battle_run(user, tokens)

        self.respond(user.nick, e.target, message)

    def run(self, command, channel=None):
        """ kind of motherfucking admin console """
        name = "motherfucking_admin"
        tokens = deque(command.split())
        if not channel:
            message = self.actions.admin_run(tokens)

        elif channel == IRC_MAIN_CHANNEL:
            message = self.actions.main_channel_run(name, tokens)

        else:
            message = self.actions.battle_run(name, tokens)

        self.write(channel, message)

    def write(self, channel, message):
        for line in message.split('\n'):
            print("#%s %s: %s" % (channel, IRC_GM_NICK, line))
            self.connection.privmsg(channel, line)

    def respond(self, nick, channel, message):
        print("#%s %s: %s" % (channel, nick, message))
        self.connection.privmsg(channel, "%s: %s" % (nick, message))

    def _ask_nickserv(self, nickname):
        pass

    def on_nickserv_reply(self, nickname, verified):
        pass


    def nick(self, source):
        return source.split('!')[0]


    #def create_pokemon(self, create_func):
        #self.create_func(self, "pikachu")
