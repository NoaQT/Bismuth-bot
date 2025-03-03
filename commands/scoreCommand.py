import utils
from commands.common.server import get_or_default, scoreboard_nbt


async def command(interaction, objective_name, server_id, db_engine):
    scores = {}
    nbt_file = scoreboard_nbt(get_or_default(db_engine, server_id))
    for player in nbt_file["data"]["PlayerScores"]:
        if player["Objective"].value == objective_name and player["Name"].value != "Total":
            scores[player["Name"].value] = player["Score"].value

    image = utils.generate_image(objective_name, scores)
    await interaction.response.send_message(file=image)
