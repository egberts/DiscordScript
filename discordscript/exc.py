from os import _exit as exit


class DiscordScriptException:
    def __init__(self, message=""):
        print(f"\033[31m\033[1m{self.__class__.__name__}:\033[0m {message}")
        exit(0)


class SyntaxError(DiscordScriptException):
    pass


class ArgumentError(DiscordScriptException):
    pass


class StatementError(DiscordScriptException):
    pass


class UnknownError(DiscordScriptException):
    pass


class AccessError(DiscordScriptException):
    pass


class ConflictError(DiscordScriptException):
    pass


class _SignalAbort(BaseException):
    pass
