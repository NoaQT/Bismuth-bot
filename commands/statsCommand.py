import os, json, difflib, utils

class statsCommand(object):
    def __init__(self, stats_folder, player_cache, stats_list):
        self.stats_folder = stats_folder
        self.player_cache = player_cache
        self.stats_list = stats_list
        
    async def Command(self, message, args):
        if args == None or len(args) != 1:
            await message.channel.send("Invalid usage")
            return

        stat_name = difflib.get_close_matches(args[0], self.stats_list, 1)

        if not stat_name:
            await message.channel.send("`Stat not found`")
            return

        stat_name = stat_name[0]
        stats = {}

        for file in os.listdir(self.stats_folder):
            uuid = file[:-5]
            if uuid not in self.player_cache: continue
            
            with open(os.path.join(self.stats_folder, file), "r") as f:
                try:
                    value = json.load(f)[stat_name]
                    player_name = self.player_cache[uuid]
                    stats[player_name] = value
                except KeyError:
                    continue
                except json.decoder.JSONDecodeError:
                    continue
        
        name_split = stat_name.split(".")
        if len(name_split) > 3:
            stat_name = name_split[1] + " " + name_split[3]
        
        f = utils.generate_image(stat_name, stats)
        await message.channel.send(file=f)

    def desc(self): return "Shows a list of all the players values for the statistic and the total"
    
    def usage(self): return "stat stat_name"