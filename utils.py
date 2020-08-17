import json, requests, os, discord, math, io
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm

def uuid_to_name(uuid):
    try:
        if "-" in uuid: uuid = uuid.replace("-", "")
        url = "https://api.mojang.com/user/profiles/" + uuid + "/names"
        re = requests.get(url)
        if re:
            re = json.loads(re.text)
            return re[len(re)-1]["name"]
        else:
            return None
    except:
        return None

def get_player_cache(player_list):
    players = {}
    for uuid in tqdm([player["uuid"] for player in player_list], desc="Loading player names"):
        player_name = uuid_to_name(uuid)
        players[uuid] = player_name if player_name != None else "Yeeted gamer"
    return players

def generate_image(title, values):

    players = ""
    scores = ""
    total = 0

    for player, score in sorted(values.items(), key = lambda x:x[1], reverse = True):
        players += player + "\n"
        scores += str(score) + "\n"
        total += score

    scores += str(total)

    grey = "#BFBFBF"
    red = "#FF5555"
    white = "#FFFFFF"
    spacing = -1
    font = ImageFont.truetype(font="minecraft.ttf", size = 20)

    draw = ImageDraw.Draw(Image.new("1", (1,1)))

    title_size = draw.textsize(text=title, font=font)
    players_size = draw.multiline_textsize(text=players, font=font, spacing=spacing)
    scores_size = draw.multiline_textsize(text=scores, font=font, spacing=spacing)

    width = players_size[0] + scores_size[0] + 20
    height = players_size[1] + 19

    image = Image.new("RGB", (width, height), color="#2c2f33")

    draw = ImageDraw.Draw(image)

    title_pos = (math.floor((width - title_size[0]) / 2), -3)
    players_pos = (2, 14)
    scores_pos = (width - scores_size[0] - 1, 14)
    total_pos = (2, players_size[1] - 4)

    draw.text(title_pos, text=title, font=font, fill=white)
    draw.text(total_pos, text="Total", font=font, fill=white)
    draw.multiline_text((players_pos), players, font=font, fill=grey, spacing=-1)
    draw.multiline_text((scores_pos), scores, font=font, align="right", fill=red, spacing=-1)

    final_buffer = io.BytesIO()
    image.save(final_buffer, "png")
    final_buffer.seek(0)

    return discord.File(filename="gay.png", fp=final_buffer)