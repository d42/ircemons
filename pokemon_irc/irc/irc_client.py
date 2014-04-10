import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from pokemon_irc.settings import IRC_SERVER, IRC_PORT, IRC_MAIN_CHANNEL, IRC_GM_NICK, IRC_REALNAME, IRC_OWNER
from pokemon_irc.game.actions import GMActions
from collections import deque


class Authorization:

    def check_auth(self, user_name):
        return user_name


def get_nick(source):
    nick, host = source.split('!', 1)
    if not host: raise('jp2gmd')
    return nick

auth = Authorization()

class PokeBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, realname=None, server=IRC_SERVER, port=IRC_PORT):

        if not realname:
            realname = "herp derp"
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    #def on_nicknameinuse(self, c, e):
        #c.nick(c.get_nickname() + "_")

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



class GMBot(irc.bot.SingleServerIRCBot):
    auth = auth

    def __init__(
        self,
        channel=IRC_MAIN_CHANNEL,
        nickname=IRC_GM_NICK,
        realname=IRC_REALNAME,
        server=IRC_SERVER,
        port=6667):

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


    def on_pubmsg(self, c, e):
        nick = get_nick(e.source)
        dest, message = e.arguments[0].split(':', 1)

        if dest != IRC_GM_NICK: return  # TODO:

        nickserv_auth = self.auth.check_auth(nick)

        if not nickserv_auth:
            self.respond(nick, e.target, "auth to nickserv plx")
            return

        tokens = deque(message.split())

        # #channel_name
        # ^ I don't like this :3

        if e.target == IRC_MAIN_CHANNEL:
            message = self.actions.main_channel_run(nickserv_auth, tokens)
        else:
            message = self.actions.battle_run(nickserv_auth, tokens)

        self.respond(nick, e.target, message)

    def run(self, command, channel=None):
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
    

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection



