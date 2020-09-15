import os
from nbt import nbt
from discord.ext import commands
from commands import scoreCommand, statsCommand, searchCommand, storageCommand

class basic(commands.Cog):
    def __init__(self, world_folder, player_cache, stats_list, member_role):
        self.world_folder = world_folder
        self.player_cache = player_cache
        self.stats_list = stats_list
        self.member_role = member_role
        self.data_folder = os.path.join(world_folder, "data")
        self.stats_folder = os.path.join(world_folder, "stats")
        nbt_file = nbt.NBTFile(os.path.join(self.data_folder, "scoreboard.dat"))["data"]
        self.objectives = [objective['Name'].value for objective in nbt_file["Objectives"]]
        self.storage_command = storageCommand.storageCommand(self.world_folder)

    def is_member(ctx):
        role = ctx.guild.get_role(ctx.cog.member_role)
        return role in ctx.message.author.roles
        
    @commands.command(
    help="Shows all of the scores of the objective and the total"
    )
    async def score(self, ctx, objective_name):
        return await scoreCommand.command(ctx, objective_name, self.data_folder, self.objectives)

    @commands.command(
    help="Shows a list of all the players values for the statistic and the total"
    )
    async def stat(self, ctx, stat_name):
        return await statsCommand.command(ctx, stat_name, self.stats_folder, self.player_cache, self.stats_list)

    @commands.command(
    help="List all the statistic/objectives with the key",
    usage="stat/objective key page"
    )
    async def search(self, ctx, *args):
        return await searchCommand.command(ctx, args, self.objectives, self.stats_list)

    @commands.command(
        name="list",
        help="Display all the currently online players"
    )
    async def listCommand(self, ctx):
        pass #Implemented on the server

    @commands.group(
        help="Display item counts from survival"
    )
    async def storage(self, ctx):
        if not ctx.invoked_subcommand:
            raise commands.errors.MissingRequiredArgument

    @storage.command(
        help="Adds a new storage location"
    )
    @commands.check(is_member)
    async def add(self, ctx, dimension: str, name: str, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int):
        return await self.storage_command.add(ctx, name, dimension, x1, y1, z1, x2, y2, z2)

    @storage.command(
        help="Removes a storage location"
    )
    @commands.check(is_member)
    async def remove(self, ctx, name):
        return await self.storage_command.remove(ctx, name)

    @storage.command(
        help="Display items from a storage location",
        usage="<name> <page>/<item_name>"
    )
    async def show(self, ctx, name, arg=None):
        return await self.storage_command.show(ctx, name, arg)

    @storage.command(
        help="List all storage locations",
        name="list"
    )
    async def list_locations(self, ctx):
        return await self.storage_command.list_locations(ctx)

    @storage.command(
        help="Display info on a storage location"
    )
    async def info(self, ctx, name):
        return await self.storage_command.info(ctx,name)