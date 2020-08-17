import os
from nbt import nbt
from discord.ext import commands
from commands import scoreCommand, statsCommand, searchCommand

class basic(commands.Cog):
    def __init__(self, world_folder, player_cache, stats_list):
        self.stats_list = stats_list
        self.data_folder = os.path.join(world_folder, "data")
        self.stats_folder = os.path.join(world_folder, "stats")
        nbt_file = nbt.NBTFile(os.path.join(self.data_folder, "scoreboard.dat"))["data"]
        self.objectives = [objective['Name'].value for objective in nbt_file["Objectives"]]
        self.player_cache = player_cache
        self.player_names = [player["name"] for player in player_cache]
        
    @commands.command(
    help="Shows all of the scores of the objective and the total"
    )
    async def score(self, ctx, objective_name):
        return await scoreCommand.command(ctx, objective_name, self.data_folder, self.player_names, self.objectives)

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