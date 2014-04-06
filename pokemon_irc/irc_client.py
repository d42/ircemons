#! /usr/bin/env python
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
irc.bot.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr



class PokeBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        derp = ['privnotice']
        self.connection.add_global_handler('privnotice', self.on_privnotice)
        self.connection.add_global_handler('pubnotice', self.on_privnotice)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        nick = self.nick(e.source)
        print(nick)
        self.connection.privmsg('nickserv', 'info %s' % nick)
        self.do_command(e, e.arguments[0])

    def on_privnotice(self, c, e):
        print(e.arguments)

    def on_pubmsg(self, c, e):
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def _ask_nickserv(self, nickname):
        pass

    def on_nickserv_reply(self, nickname, verified):
        pass


    def nick(self, source):
        return source.split('!')[0]
    

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        #if cmd == "disconnect":
            #self.disconnect()
        #elif cmd == "die":
            #self.die()
        #elif cmd == "stats":
            #for chname, chobj in self.channels.items():
                #c.notice(nick, "--- Channel statistics ---")
                #c.notice(nick, "Channel: " + chname)
                #users = chobj.users()
                #users.sort()
                #c.notice(nick, "Users: " + ", ".join(users))
                #opers = chobj.opers()
                #opers.sort()
                #c.notice(nick, "Opers: " + ", ".join(opers))
                #voiced = chobj.voiced()
                #voiced.sort()
                #c.notice(nick, "Voiced: " + ", ".join(voiced))
        #elif cmd == "dcc":
            #dcc = self.dcc_listen()
            #c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                #ip_quad_to_numstr(dcc.localaddress),
                #dcc.localport))
        #else:
            #c.notice(nick, "Not understood: " + cmd)

def main():
    server = "irc.freenode.net"
    channel = "#kekchan"
    nickname = "kekbot"
    port = 6667

    bot = PokeBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
