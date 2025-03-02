import os
from nbt import nbt
from discord.ext import commands
from discord import app_commands
from commands import scoreCommand, statsCommand, searchCommand, storageCommand


class basic(commands.Cog):
    def __init__(self, world_folder, db_engine, stats_list, member_role):
        self.world_folder = world_folder
        self.db_engine = db_engine
        self.player_cache = {}
        self.stats_list = stats_list
        self.member_role = member_role
        self.data_folder = os.path.join(world_folder, "data")
        self.stats_folder = os.path.join(world_folder, "stats")
        nbt_file = nbt.NBTFile(os.path.join(self.data_folder, "scoreboard.dat"))["data"]
        self.objectives = [objective['Name'].value for objective in nbt_file["Objectives"]]
        self.storage_command = storageCommand.StorageCommand(self.world_folder)

    def is_member(ctx):
        role = ctx.guild.get_role(ctx.cog.member_role)
        return role in ctx.message.author.roles

    @app_commands.command(
        description="Shows all of the scores of the objective and the total"
    )
    async def score(self, interaction, objective: str):
        return await scoreCommand.command(interaction, objective, self.data_folder, self.objectives)

    @app_commands.command(
        description="Shows a list of all the players values for the statistic and the total"
    )
    async def stat(self, interaction, stat: str):
        return await statsCommand.command(interaction, stat, self.db_engine, self.stats_folder, self.player_cache, self.stats_list)

    @app_commands.command(
        description="List all the statistic/objectives with the key",
    )
    async def search(self, interaction, target: str, key: str, page: int):
        return await searchCommand.command(interaction, target, key, page, self.objectives, self.stats_list)

    @app_commands.command(
        name="list",
        description="Display all the currently online players"
    )
    async def listCommand(self, interaction):
        pass  # Implemented on the server

    storage = app_commands.Group(name="storage", description="Display item counts from survival")

    @storage.command(
        description="Adds a new storage location"
    )
    @commands.check(is_member)
    async def add(self, interaction, dimension: str, name: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int):
        return await self.storage_command.add(interaction, name, dimension, x1, y1, z1, x2, y2, z2)

    @storage.command(
        description="Removes a storage location"
    )
    @commands.check(is_member)
    async def remove(self, interaction, name: str):
        return await self.storage_command.remove(interaction, name)

    @storage.command(
        description="Display items from a storage location",
    )
    async def show(self, interaction, name: str, arg: str=None):
        return await self.storage_command.show(interaction, name, arg)

    @storage.command(
        description="List all storage locations",
        name="list"
    )
    async def list_locations(self, interaction):
        return await self.storage_command.list_locations(interaction)

    @storage.command(
        description="Display info on a storage location"
    )
    async def info(self, interaction, name: str):
        return await self.storage_command.info(interaction, name)

