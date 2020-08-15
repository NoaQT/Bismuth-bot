import discord, difflib, os, utils
from nbt import nbt

class scoreCommand(object):
    def __init__(self, data_folder, players):
        self.data_folder = data_folder
        self.players = players

    async def Command(self, message, args):
        if len(args) != 1:
            await message.channel.send("Invalid usage")
            return

        nbt_file = nbt.NBTFile(os.path.join(self.data_folder, "scoreboard.dat"))["data"]
        objective = difflib.get_close_matches(args[0], [objective['Name'].value for objective in nbt_file["Objectives"]], 1)

        if not objective:
            await message.channel.send("`Scoreboard not found`")
            return

        objective = objective[0]

        scores = {}

        for player in nbt_file["PlayerScores"]:
            if player["Objective"].value == objective and player["Name"].value in self.players:
                scores[player["Name"].value] = player["Score"].value

        image = utils.generate_image(objective, scores)
        await message.channel.send(file=image)
        
    def desc(self): return "Shows all of the scores of the objective and the total"
    
    def usage(self): return "score objective_name"