import os, discord
from nbt import nbt

class searchCommand(object):
    def __init__(self, data_folder, stat_list):
        nbt_file = nbt.NBTFile(os.path.join(data_folder, "scoreboard.dat"))["data"]
        self.objectives = [objective['Name'].value for objective in nbt_file["Objectives"]]
        self.stat_list = stat_list

    async def Command(self, message, args):
        if not args:
            await message.channel.send("Invalid usage")
            return 

        search_list = []
        if args[0] == "stat":
            search_list = self.stat_list
        elif args[0] == "objective":
            search_list = self.objectives
        else:
            await message.channel.send("Can only search for statistics or objectives")
            return

        page = 1
        if args[len(args) - 1].isdigit():
            page = int(args[len(args) - 1])
        
        key = args[1] if len(args) > 1 and not args[1].isdigit() else ""

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
            await message.channel.send("None found")
            return
        
        response = str(search_result[page - 1])[1:][:-1].replace("'", "")
        footer_text = "Showing page " + str(page) + "/" + str(len(search_result))

        embed = discord.Embed(colour = 0x9e42f5,
        description = "```" + response + "```"
        )

        embed.set_author(
            name = key if key else "\u200b",
            icon_url = "https://cdn.discordapp.com/icons/635252849571266580/a_a0834de4803ce4a74fa2f7a6d456f39a.png"
        )

        embed.set_footer(text=footer_text)

        await message.channel.send(embed=embed)

    def desc(self): return "List all the statistic/objectives with the key"
    
    def usage(self): return "search stat/objective key page"