Simport json, requests, os, discord, math, io
from PIL import ImageFont, ImageDraw, Image 

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

def get_player_cache(uuidlist):
    players = {}
    for uuid in uuidlist:
        player_name = uuid_to_name(uuid)
        print(player_name)
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

def format_discord_message(discordmessage):
    args = [""]
    args.append({"text" : "<"})
    args.append({
        "text" : discordmessage.author.name,
        "color" : "gray"
    })
    args.append({"text" : "> "})

    for mention in discordmessage.mentions:
        discordmessage.content = discordmessage.content.replace("<@" + str(mention.id) + ">", "@" + mention.name)

    for word in discordmessage.content.split(" "):
        if word.startswith("http") and validators.url(word) == True:
            args.append({
                "text" : word,
                "color" : "aqua",
                "clickEvent" : {"action" : "open_url", "value" : word},
                "hoverEvent" : {"action" : "show_text", "value" : "Goto url"}
            })
            args.append({"text" : " "})

        else:
            args[len(args) - 1]["text"] += word + " "

    for attachment in discordmessage.attachments:
        args.append({
                "text" : "attachment ",
                "color" : "aqua",
                "clickEvent" : {"action" : "open_url", "value" : attachment.url},
                "hoverEvent" : {"action" : "show_text", "value" : "Open attachment"}
            })

    return "tellraw @a " + str(json.dumps(args))

def format_response_message(author, message):
    return 'tellraw ' + author + ' ["",{"text":"' + message + '","color":"gray"}]'

def list_to_string(list):
    return str(list)[1:][:-1].replace("'", "")

def get_matches(arr, name, max_length, get_all=False):
    re = []
    re1 = []
    for item in arr:
        if get_all or name in item:
            re1.append(item)

            if len(str(re1)) > max_length:
                re.append(re1)
                re1 = []
    
    if re1: 
        re.append(re1)

    elif not re:
        re = None

    return re

def list_base(args, stats, objectives):
    re = None
    i = 1
        
    if args[0] == "stat":
        if len(args) == 1 or args[1].isdigit():
            re = get_matches(stats, "", 500, True)
            if re:
                if len(args) > 1:
                    i = args[1]
                    try:
                        i2 = int(args[1]) - 1 
                        if i2 < 0: raise IndexError
                        re1 = list_to_string(re[i2])
                    except IndexError:
                        re1 = "page doesn't exist"
                        i = None
                else:
                    re1 = list_to_string(re[0])
            else:
                re1 = "None found"

        else: 
            re = get_matches(stats, args[1], 500)
            if re:
                if len(args) > 2:
                    i = args[2]
                    try:
                        i2 = int(args[2]) - 1 
                        if i2 < 0: raise IndexError
                        re1 = list_to_string(re[int(args[2])-1])
                    except IndexError:
                        re1 = "page doesn't exist"
                        i = None
                else:
                    re1 = list_to_string(re[0])
            else:
                re1 = "None found"


    elif args[0] == "objective":
        if len(args) == 1 or args[1].isdigit():
            re = get_matches(objectives, "", 500, True)
            if re:
                if len(args) > 1:
                    i = args[1]
                    try:
                        i2 = int(args[1]) - 1 
                        if i2 < 0: raise IndexError
                        re1 = list_to_string(re[int(args[1])-1])
                    except IndexError:
                        re1 = "page doesn't exist"
                        i = None
                else:
                    re1 = list_to_string(re[0])
            else:
                re1 = "None found"

        else: 
            re = get_matches(objectives, args[1], 500)
            if re:
                if len(args) > 2:
                    i = args[2]
                    try:
                        i2 = int(args[2]) - 1 
                        if i2 < 0: raise IndexError
                        re1 = list_to_string(re[int(args[2])-1])
                    except IndexError:
                        re1 = "page doesn't exist"
                        i = None
                else:
                    re1 = list_to_string(re[0])
            else:
                re1 = "None found"

    else:
        re1 = "Can only list stats or objectives"

    if not re and re1 != "Can only list stats or objectives": 
        re1 = "None found"

    return [re, re1, i]