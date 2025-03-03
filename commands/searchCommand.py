import discord, utils
from sqlalchemy.util import await_only

from commands.common import Pagination
from commands.common.server import get_or_default, scoreboard_nbt


async def command(interaction, target, key, server_id, db_engine, stat_list):
    if target == "Statistics":
        search_list = stat_list
    else:
        nbt_file = scoreboard_nbt(get_or_default(db_engine, server_id))
        search_list = [objective['Name'].value for objective in nbt_file["data"]["Objectives"]]

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

    if not search_result:
        return await interaction.response.send_message("No results")

    return await Pagination(interaction, get_page, len(search_result)).view()
