import os, discord, json, utils
from commands import scoreCommand, statsCommand, searchCommand, helpCommand
from discord.ext import commands

with open("config.json", "r") as f:
    cfg = json.load(f)

TOKEN = cfg["bot"]["token"]
PREFIX = cfg["bot"]["prefix"]
SERVER_FOLDER = cfg["server"]["path_to_server_folder"]
WORLD_NAME = cfg["server"]["world_name"]
WORLD_FOLDER = os.path.join(SERVER_FOLDER, WORLD_NAME)
STATS_FOLDER = os.path.join(WORLD_FOLDER, "stats")
DATA_FOLDER = os.path.join(WORLD_FOLDER, "data")

with open(os.path.join(SERVER_FOLDER, "whitelist.json"), "r") as f:
    whitelist = json.load(f)

with open("list.json", "r") as f:
    playerlist = json.load(f)
    
with open("list.json", "w+") as f:
    playerlist = playerlist + [player for player in whitelist if player not in playerlist]
    f.write(json.dumps(playerlist))

PLAYERS = [player["uuid"] for player in playerlist]
PLAYERNAMES = [player["name"] for player in playerlist]

Bot = commands.Bot(command_prefix=PREFIX)

player_cache = utils.get_player_cache(PLAYERS)

with open("stats_list.txt", "r") as f:
    stats_list = [stat for stat in f.read().split("\n")]

commandsdict = {}
commandsdict["score"] = scoreCommand.scoreCommand(DATA_FOLDER, PLAYERNAMES)
commandsdict["stat"] = statsCommand.statsCommand(STATS_FOLDER, player_cache, stats_list)
commandsdict["search"] = searchCommand.searchCommand(DATA_FOLDER, stats_list)
commandsdict["help"] = helpCommand.helpCommand()
commandsdict["help"].init(commandsdict)

@Bot.event
async def on_ready():
    print("ready")
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game(name=PREFIX + "help"))

@Bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(PREFIX):        
        args = message.content.lower().strip()[len(PREFIX):].split(" ")
    
        commandname = args[0]

        if commandname in commandsdict:
            args = args[1:] if len(args) > 1 else None
            await commandsdict[commandname].Command(message, args)

        else:
            await message.channel.send("Command not found\nDo `" + PREFIX + "help` for a list of commands")

Bot.run(TOKEN)