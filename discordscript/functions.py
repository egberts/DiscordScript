from .exc import *
from .exc import _SignalAbort
import asyncio


async def say(client, msg, args, env):
    await client.send_message(msg.channel, "".join(args))


async def log(client, msg, args, env):
    print("".join(args))


async def input(client, msg, args, env):
    timeout = None
    if len(args) >= 1:
        try:
            timeout = abs(int(args[0]))
        except:
            ArgumentError("Invalid Timeout")
    return (await client.wait_for_message(timeout=timeout, author=msg.author, channel=msg.channel)).content


async def delay(client, msg, args, env):
    assert len(args) == 1
    try:
        int(args[0])
    except:
        ArgumentError("Invalid delay for \033[34mdelay\033[0m")
    await asyncio.sleep(int(args[0]))


async def exit(client, msg, args, env):
    raise _SignalAbort()


async def require(client, msg, args, env):
    if len(args) < 2:
        ArgumentError("No arguments specified")
    try:
        res = args[0] == args[1]
    except:
        ArgumentError("Incomparable arguments")
    if not res:
        raise _SignalAbort()


FUNCTIONS = {"say": say, "delay": delay, "exit": exit, "require": require, "log": log, "input": input}
