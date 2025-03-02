import difflib
import os
import utils

from nbt import nbt


async def command(interaction, objective_name, data_folder, objectives):
    if objective_name not in objectives:
        await interaction.response.send_message("`Scoreboard not found`")
        return

    objective_name = objective_name[0]

    scores = {}

    nbt_file = nbt.NBTFile(os.path.join(data_folder, "scoreboard.dat"))["data"]
    for player in nbt_file["PlayerScores"]:
        if player["Objective"].value == objective_name and player["Name"].value != "Total":
            scores[player["Name"].value] = player["Score"].value

    image = utils.generate_image(objective_name, scores)
    await interaction.response.send_message(file=image)
