#!/usr/bin/env python3

import os, discord, json, utils
from commands import basic
from discord.ext import commands

with open("config.json", "r") as f:
    cfg = json.load(f)

TOKEN = cfg["bot"]["token"]
PREFIX = cfg["bot"]["prefix"]
MEMBER_ROLE = cfg["bot"]["member_role"]
SERVER_FOLDER = cfg["server"]["path_to_server_folder"]
WORLD_NAME = cfg["server"]["world_name"]
WORLD_FOLDER = os.path.join(SERVER_FOLDER, WORLD_NAME)

uuid_list = [file[:-5] for file in os.listdir(os.path.join(WORLD_FOLDER, "stats"))]
player_cache = utils.get_player_cache(uuid_list)

with open("stats_list.txt", "r") as f:
    stats_list = f.read().split("\n")

Bot = commands.Bot(
    command_prefix=PREFIX,
    case_insensitive=True
    )

@Bot.event
async def on_ready():
    Bot.add_cog(basic.basic(WORLD_FOLDER, player_cache, stats_list, MEMBER_ROLE))

    print(f'Logged in as {Bot.user.name} - {Bot.user.id}')
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game(name=PREFIX + "help"))

@Bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("`Command not found`")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send("`insufficient permission`")
    elif isinstance(error, commands.errors.UserInputError):
        await ctx.send("`Invalid usage`")
    else:
        raise error

@Bot.event
async def on_command(ctx):
    print(f"{ctx.message.created_at} {ctx.message.author} {ctx.message.content}")

print("Starting bot")
Bot.run(TOKEN)