import discord, utils
from discord.ext import commands
from .common import Pagination


async def command(interaction, target, key, objectives, stat_list):
    if target == "Statistics":
        search_list = stat_list
    else:
        search_list = objectives

    search_result = []
    temp = []
    length = 0

    for item in search_list:
        if key in item:
            temp.append(item)
            length += len(item)

            if length > 1500:
                search_result.append(temp)
                temp = []
                length = 0

    if temp:
        search_result.append(temp)

    async def get_page(page: int):
        response = str(search_result[page - 1])[1:][:-1].replace("'", "")
        return utils.generate_embed(f"{target}: {key if key else '\u200b'}", response, icon_url=interaction.guild.icon and interaction.guild.icon.url)

    return await Pagination(interaction, get_page, len(search_result)).view()
