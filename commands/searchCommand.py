import discord, utils
from discord.ext import commands


async def command(interaction, target, key, page, objectives, stat_list):
    search_list = []
    if target == "stat":
        search_list = stat_list
    elif query == "objective":
        search_list = objectives
    else:
        await interaction.response.send_message("`Can only search for statistics or objectives`")
        return

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

    if page > len(search_result):
        await interaction.response.send_message("`None found`")
        return

    response = str(search_result[page - 1])[1:][:-1].replace("'", "")
    footer_text = "Showing page " + \
                  str(page) + "/" + str(len(search_result))

    await interaction.response.send_message(embed=utils.generate_embed(key if key else "\u200b", response, footer_text, interaction.guild.icon and interaction.guild.icon.url))
