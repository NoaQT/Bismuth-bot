#!/usr/bin/env python3

import discord
import json
import os
import utils
import sqlalchemy

from discord.ext import commands

from commands import basic
from db import models

with open("config.json", "r") as f:
    cfg = json.load(f)

TOKEN = cfg["bot"]["token"]
PREFIX = cfg["bot"]["prefix"]
MEMBER_ROLE = cfg["bot"]["member_role"]

with open("stats_list.txt", "r") as f:
    stats_list = f.read().split("\n")

intents = discord.Intents.all()

Bot = commands.Bot(
    command_prefix=PREFIX,
    case_insensitive=True,
    intents=intents
)

db_engine = sqlalchemy.create_engine(cfg["database"]["conn"]) 
models.Base.metadata.create_all(db_engine)

@Bot.event
async def on_ready():
    await Bot.add_cog(basic.basic(db_engine, stats_list, MEMBER_ROLE))

    print(f'Logged in as {Bot.user.name} - {Bot.user.id}')
    await Bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Bismuth"))

    synced = await Bot.tree.sync()
    print(f"Synced {len(synced)} commands")

    await utils.refresh_player_names(db_engine)


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
