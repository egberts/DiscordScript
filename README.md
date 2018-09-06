# DiscordScript
DiscordScript is a simple DSL/Scripting Language for writing Discord Bots (VERY unstable/beta).
## Prerequisites
* Python (3.6 or greater)
* Pip
* discord.py
* TatSu
## Installation
#### with Pip
```
python3.6 -m pip install DiscordScript
```
#### without Pip
```
git clone https://github.com/jcb1317/DiscordScript.git
cd DiscordScript
python3.6 setup.py install
```

## Basic Usage
#### Ping Command
* First, create a bot and get a bot token from [the Discord Developer Platform](https://discordapp.com/developers/applications/me)
* Add the bot to a Server and give it permissions to read and write in a channel
* Install Discord Script if you haven't done it before
* Create a file named `test.ds` and open it
```
@token:YOUR_TOKEN;
@prefix:!;

!ping {
   say "Pong!";
}
```
* Write this into your file and replace `YOUR_TOKEN` with the bot token from before
* Navigate to `test.ds`' directory and user `discordscript test.ds`
* Test the Bot in the Server you added it to before
* When you're finished, hit `Ctrl+C` to quit
