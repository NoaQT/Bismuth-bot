import discord
import io
import json
import math
import requests

from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm


def uuid_to_name(uuid):
    try:
        if "-" in uuid: uuid = uuid.replace("-", "")
        url = "https://api.mojang.com/user/profiles/" + uuid + "/names"
        re = requests.get(url)
        if re:
            re = json.loads(re.text)
            return re[len(re) - 1]["name"]
        else:
            return None
    except:
        return None


def get_player_cache(player_list):
    players = {}
    for uuid in tqdm(player_list, desc="Loading player names"):
        break
        player_name = uuid_to_name(uuid)
        players[uuid] = player_name if player_name else "Yeeted gamer"
    return players


def generate_image(title, values):
    players = ""
    scores = ""
    total = 0

    for player, score in sorted(values.items(), key=lambda x: x[1], reverse=True):
        players += player + "\n"
        scores += str(score) + "\n"
        total += score

    scores += str(total)

    grey = "#BFBFBF"
    red = "#FF5555"
    white = "#FFFFFF"
    spacing = -1
    font = ImageFont.truetype(font="minecraft.ttf", size=20)

    draw = ImageDraw.Draw(Image.new("1", (1, 1)))

    title_bb = draw.textbbox((0, 0), text=title, font=font)
    players_bb = draw.multiline_textbbox((0, 0), text=players, font=font, spacing=spacing)
    scores_bb = draw.multiline_textbbox((0, 0), text=scores, font=font, spacing=spacing)

    title_size = title_bb[2] - title_bb[0], title_bb[3] - title_bb[1] 
    players_size = players_bb[2] - players_bb[0], players_bb[3] - players_bb[1] 
    scores_size = scores_bb[2] - scores_bb[0], scores_bb[3] - scores_bb[1] 

    width = players_size[0] + scores_size[0] + 20
    height = scores_size[1] + 19

    image = Image.new("RGB", (width, height), color="#2c2f33")

    draw = ImageDraw.Draw(image)

    title_pos = (math.floor((width - title_size[0]) / 2), -3)
    players_pos = (2, 14)
    scores_pos = (width - scores_size[0] - 1, 14)
    total_pos = (2, scores_size[1] + 1)

    draw.text(title_pos, text=title, font=font, fill=white)
    draw.text(total_pos, text="Total", font=font, fill=white)
    draw.multiline_text((players_pos), players, font=font, fill=grey, spacing=-1)
    draw.multiline_text((scores_pos), scores, font=font, align="right", fill=red, spacing=-1)

    final_buffer = io.BytesIO()
    image.save(final_buffer, "png")
    final_buffer.seek(0)

    return discord.File(filename="gay.png", fp=final_buffer)


def generate_embed(author="\u200b", description="", footer_text=""):
    embed = discord.Embed(
        colour=0x9e42f5,
        description="```" + description + "```"
    )

    embed.set_author(
        name=author,
        icon_url="https://cdn.discordapp.com/icons/635252849571266580/a_a0834de4803ce4a74fa2f7a6d456f39a.png"
    )

    embed.set_footer(text=footer_text)

    return embed
