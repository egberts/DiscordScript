from .functions import FUNCTIONS
from abc import ABC, abstractmethod
from .exc import *

TOKEN_TABLE = {}


class BaseToken(ABC):
    def __init_subclass__(cls, tkn):
        TOKEN_TABLE[tkn] = cls

    def __init__(self, obj, pt):
        self.obj = obj
        self.type = obj["type"]
        self._body = obj["content"]
        self.pt = pt
        self.body = []
        self._parse()

    @abstractmethod
    def _parse(self):
        pass

    async def call(self, env):
        pass


class Command(BaseToken, tkn="command"):
    def _parse(self):
        for token in self._body:
            self.body.append(self.pt[token["type"]](token, self.pt))

    async def call(self, env):

        for token in self.body:
            await token.call(env)


class If(BaseToken, tkn="if"):
    def _parse(self):
        self.cond = Logic(self.obj["condition"], self.pt)
        for token in self._body:
            self.body.append(self.pt[token["type"]](token, self.pt))

    async def call(self, env):
        if await self.cond.call(env):
            for token in self.body:
                await token.call(env)


class Function(BaseToken, tkn="function"):
    def _parse(self):
        if self._body[0] not in FUNCTIONS.keys():
            StatementError(f"Invalid function: \033[34m{self._body[0]}\033[0m")
        self.args = []
        for token in self._body[1]:
            self.args.append(self.pt[token["type"]](token, self.pt))
        self.func = FUNCTIONS[self._body[0]]

    async def call(self, env):
        return await self.func(env.client, env.msg, [await i.call(env) for i in self.args], env)


class Logic(BaseToken, tkn="logic"):
    def __init__(self, obj, pt):
        super(Logic, self).__init__(obj, pt)
        self.staticop = None

    def _parse(self):
        if len(self._body) == 1:
            self.staticop = Bool(self._body[0], self.pt)
        else:
            self.args = []
            for token in self._body:
                self.args.append(self.pt[token["type"]](token, self.pt))

    async def call(self, env):
        if self.staticop is not None:
            return self.staticop
        op = await (self.args[1]).call(env)
        return eval(f"a {op} b", {"a": await (self.args[0]).call(env), "b": await (self.args[2]).call(env)})


class LogicOperator(BaseToken, tkn="logic_op"):
    operators = {
        "is": "==", "!is": "!=", "in": "in", "!in": "not in"
    }

    def __init__(self, obj, pt):
        super(LogicOperator, self).__init__(obj, pt)

    def _parse(self):
        pass

    async def call(self, env):
        return self.operators[self._body]


class String(BaseToken, tkn="string"):
    def _parse(self):
        self.value = self.obj["content"]

    async def call(self, env):
        return self.value


class Id(BaseToken, tkn="id"):
    def _parse(self):
        self.value = self.obj["content"]

    async def call(self, env):
        return int(self.value)


class Object(BaseToken, tkn="object"):
    def _parse(self):
        self.value = self.obj["content"]

    async def call(self, env):
        if self.value[0] not in env.keys():
            UnknownError(f"Constant \033[34m{self.value[0]}\033[0m not found")
        cwo = env[self.value[0]]
        for i in self.value[1:]:
            try:
                if not i.startswith("_"):
                    cwo = getattr(cwo, i)
                else:
                    AccessError("Accessing internal attributes is forbidden")
            except:
                UnknownError("Unknown attribute")
        return cwo


class Argument(BaseToken, tkn="argument"):
    def _parse(self):
        self.value = self._body

    async def call(self, env):
        if self.value == "@":
            return " ".join(env.args)
        try:
            int(self.value)
            return env.args.get(int(self.value), "")
        except:
            if self.value in env.vars.keys():
                return env.vars[self.value]
            ArgumentError("Unknown Variable")


class Bool(BaseToken, tkn="bool"):
    def _parse(self):
        self.value = self.obj["content"]

    async def call(self, env):
        if self.value == "true":
            return True
        else:
            return False


class Assignment(BaseToken, tkn="assignment"):
    def _parse(self):
        self.varname = self.obj["name"].strip()
        self.varval = self.pt[self._body["type"]](self._body, self.pt)

    async def call(self, env):
        if self.varname in env:
            ConflictError("Variable name conflicts with environment variable")
        env.vars[self.varname] = await self.varval.call(env)
