from .grammar.grammar import DiscordScriptParser
from os.path import abspath
from _io import TextIOWrapper
import discord
from .tokens import *
from .exc import SyntaxError, _SignalAbort
from builtins import exit as ex


class Client(discord.Client):
    def __init__(self, file, log=False):
        super(Client, self).__init__()
        self._log = log
        self.parser = DiscordScriptParser()
        if type(file) == TextIOWrapper:
            self.ast = self.parser.parse(file.read())
        else:
            with open(abspath(file), "r") as f:
                self.ast = self.parser.parse(f.read())
        self.parse()

    def parse(self):
        self.commands = {}
        self.conf = {}
        for i in self.ast:
            if i["type"] == "command":
                self.commands[i["name"].strip()] = Command(i, TOKEN_TABLE)
            elif i["type"] == "config":
                self.conf[i["name"].strip()] = i["content"].strip()
        if not ("prefix" in self.conf and "token" in self.conf):
            SyntaxError("Failed to specify Prefix and Token")
        self.prefix = self.conf["prefix"]
        self.token = self.conf["token"]

    def log(self, msg):
        if self._log:
            print(msg)

    def listen(self):
        try:
            self.run(self.token)
        except SystemExit:
            exit(0)

    async def on_ready(self):
        self.log("\033[34Unit ready!\033[0m")

    async def on_message(self, message):
        if not message.content.startswith(self.prefix):
            return
        if not message.content.split(" ")[0].strip() > self.prefix:
            return
        cmd = message.content.split(" ")[0].strip()[len(self.prefix):]
        if cmd not in self.commands:
            return
        try:
            await (self.commands[cmd]).call(Env(
                self, message, message.content.split()[1:]
            ))
        except _SignalAbort:
            return


class Env(dict):
    def __init__(self, client, msg, args, **kwargs):
        super(Env, self).__init__(**kwargs)
        self.client = client
        self.msg = msg
        self.args = args
        self["msg"] = Message(msg)
        self.vars = {}


class Message:
    def __init__(self, base):
        self.author = User(base.author)
        self.server = Server(base.server)
        self.content = base.content
        self._id = base.id

    def __eq__(self, other):
        if type(other) == int:
            return self._id == str(other)

    def __ne__(self, other):
        if type(other) == int:
            return self._id != str(other)


class User:
    def __init__(self, base):
        self.roles = [int(i.id) for i in base.roles]
        self.name = base.name
        self.tag = base.discriminator
        self.mention = base.mention
        self._id = base.id

    def __eq__(self, other):
        if type(other) == int:
            return self._id == str(other)

    def __ne__(self, other):
        if type(other) == int:
            return self._id != str(other)


class Server:
    def __init__(self, base):
        self.roles = [int(i.id) for i in base.roles]
        self.members = [User(i) for i in base.members]
        self.owner = User(base.owner)
        self._id = base.id
        self._base = base

    def __eq__(self, other):
        if type(other) == int:
            return self._id == str(other)

    def __ne__(self, other):
        if type(other) == int:
            return self._id != str(other)

    def __contains__(self, item):
        i = int(item)
        return (
            [i.id for i in self._base.members].__contains__(i)
        )
