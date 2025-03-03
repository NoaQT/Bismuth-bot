import discord
import io
import json
import math
import requests
import asyncio

from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import Player
from tqdm import tqdm


async def refresh_player_names(db_engine):
    while True:
        with Session(db_engine) as session:
            for player in tqdm(session.scalars(select(Player)).all(), desc="Updating player names"):
                player.name = await uuid_to_name(player.uuid)

            session.commit()

        await asyncio.sleep(60 * 24)


async def uuid_to_name(uuid):
    retries = 5
    while retries:
        url = f"https://api.minecraftservices.com/minecraft/profile/lookup/{uuid.replace('-', '')}"
        res = requests.get(url)
        if not res.ok:
            await asyncio.sleep(30)
            retries -= 1
            continue

        res = res.json()
        if "error" in res:
            return None

        return res["name"]


async def get_player_name(db_engine, uuid):
    with Session(db_engine) as session:
        player = session.scalars(
            select(Player).where(Player.uuid == uuid)
        ).first()

        if player:
            name = player.name
        else:
            name = await uuid_to_name(uuid) or "Yeeted gamer"
            session.add(Player(name=name, uuid=uuid))
            session.commit()

    return name


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


def generate_embed(author="\u200b", description="", footer_text="", icon_url=""):
    embed = discord.Embed(
        colour=0x9e42f5,
        description="```" + description + "```"
    )

    embed.set_author(
        name=author,
        icon_url=icon_url
    )

    embed.set_footer(text=footer_text)

    return embed


def parse_properties(path):
    res = {}
    with open(path) as f:
        for line in f.readlines():
            if line.startswith("#") or "=" not in line:
                continue

            line_split = line.split("=")
            res[line_split[0]] = line_split[1]

    return res
