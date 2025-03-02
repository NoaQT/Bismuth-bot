import os, json, difflib, utils


async def command(interaction, stat_name, db_engine, stats_folder, stats_list):
    if stat_name not in stats_list:
        await interaction.response.send_message("`Stat not found`")
        return

    stats = {}
    for file in os.listdir(stats_folder):
        with open(os.path.join(stats_folder, file), "r") as f:
            try:
                value = json.load(f)[stat_name]
                player_name = await utils.get_player_name(db_engine, file[:-5])
                stats[player_name] = value
            except KeyError:
                continue
            except json.decoder.JSONDecodeError:
                continue

    name_split = stat_name.split(".")
    if len(name_split) > 3:
        stat_name = name_split[1] + " " + name_split[3]

    f = utils.generate_image(stat_name, stats)
    await interaction.response.send_message(file=f)
