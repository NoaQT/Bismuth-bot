import difflib, os, utils
from nbt import nbt

async def command(self, ctx, objective_name, data_folder, players, objectives):
    objective_name = difflib.get_close_matches(objective_name, objectives, 1)

    if not objective_name:
        await ctx.send("`Scoreboard not found`")
        return

    objective_name = objective_name[0]

    scores = {}

    nbt_file = nbt.NBTFile(os.path.join(data_folder, "scoreboard.dat"))["data"]
    for player in nbt_file["PlayerScores"]:
        if player["Objective"].value == objective_name and player["Name"].value in players:
            scores[player["Name"].value] = player["Score"].value

    image = utils.generate_image(objective_name, scores)
    await ctx.send(file=image)