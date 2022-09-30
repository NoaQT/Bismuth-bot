import json, os, time, discord, utils
from datetime import datetime
from nbt.region import RegionFile


class StorageCommand(object):
    def __init__(self, world_folder):
        self.world_folder = world_folder
        self.dimension_dict = {"overworld": "region", "nether": os.path.join("DIM-1", "region"),
                               "end": os.path.join("DIM1", "region")}

        with open("config.json", "r") as f:
            cfg = json.load(f)

        self.storage_dict = cfg["storage"]
        self.cache = {}

    def save_config(self):
        with open("config.json", "r+") as f:
            cfg = json.load(f)
            cfg["storage"] = self.storage_dict
            f.seek(0)
            f.write(json.dumps(cfg, indent=4))
            f.truncate()

    async def add(self, ctx, name, dimension, x1, y1, z1, x2, y2, z2):
        if name in self.storage_dict:
            await ctx.send(f"`{name} is already used`")
            return

        if dimension not in self.dimension_dict:
            await ctx.send(f"`Invalid dimension: `{dimension}")
            return

        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        z1, z2 = sorted((z1, z2))

        self.storage_dict[name] = {
            "dimension": dimension,
            "pos1": [x1, y1, z1],
            "pos2": [x2, y2, z2]
        }
        self.save_config()

        await ctx.send(f"Added storage location {name}")

    async def remove(self, ctx, name):
        if name not in self.storage_dict:
            await ctx.send(f"`Storage location {name} doesn't exist`")
            return

        del self.storage_dict[name]
        if name in self.cache:
            del self.cache[name]

        self.save_config()

        await ctx.send(f"`Removed storage location {name}`")

    async def list_locations(self, ctx):
        description = "\n"
        for location in self.storage_dict:
            description += location + "\n"
        author = "Storage location list"
        footer_text = f"Total of {len(self.storage_dict)} storage locations"

        await ctx.send(embed=utils.generate_embed(author, description, footer_text))

    async def info(self, ctx, name):
        if name not in self.storage_dict:
            await ctx.send(f"`Storage location {name} doesn't exist`")
            return

        author = name
        description = f'Dimension: {self.storage_dict[name]["dimension"]}\n'
        description += f'From: {self.storage_dict[name]["pos1"]}\n'
        description += f'To: {self.storage_dict[name]["pos2"]}\n'
        last_update = datetime.fromtimestamp(self.cache[name]["last_update"]).isoformat(" ",
                                                                                        "seconds") if name in self.cache else "NaN"
        description += f'Last update: {last_update}'

        await ctx.send(embed=utils.generate_embed(author, description))

    async def show(self, ctx, name, arg):
        if name not in self.storage_dict:
            return await ctx.send(f"`Storage location {name} doesn't exist`")

        items = self.get_items(name)

        embed = discord.Embed(colour=0x9e42f5)
        if not arg or arg.isdigit():
            page = int(arg) if arg else 1
            page_count = len(items) // 20 + 1

            if page > page_count:
                return await ctx.send(f"`Page {page} doesn't exist`")

            if not items:
                return await ctx.send("`None`")

            items = sorted(items.items(), key=lambda x: x[1], reverse=True)

            items1 = []
            counts = []
            for i in range(page * 20 - 1, page * 20 + 19):
                if i >= len(items):
                    break
                items1.append(items[i][0])
                counts.append(str(items[i][1]))

            embed.add_field(name="Items", value="\n".join(items1), inline=True)
            embed.add_field(name="Count", value="\n".join(counts), inline=True)
            footer_text = f"Showing page {page}/{page_count} | "
            author = name
        else:
            footer_text = ""
            author = f"{name} | {arg}"

            if arg not in items:
                items[arg] = 0

            embed.description = f"{arg} : {items[arg]}"

        footer_text += f'Last update {datetime.fromtimestamp(self.cache[name]["last_update"]).isoformat(" ", "seconds")}'

        embed.set_author(
            name=author,
            icon_url="https://cdn.discordapp.com/icons/635252849571266580/a_a0834de4803ce4a74fa2f7a6d456f39a.png"
        )

        embed.set_footer(text=footer_text)

        await ctx.send(embed=embed)

    def get_items(self, name):
        if name in self.cache and time.time() - self.cache[name]["last_update"] < 300:
            return self.cache[name]["items"]

        region_folder = os.path.join(self.world_folder, self.dimension_dict[self.storage_dict[name]["dimension"]])
        x1, y1, z1 = self.storage_dict[name]["pos1"]
        x2, y2, z2 = self.storage_dict[name]["pos2"]

        items = {}
        for region_x in range(x1 // 512, x2 // 512 + 1):
            for region_z in range(z1 // 512, z2 // 512 + 1):
                region = RegionFile(os.path.join(region_folder, f"r.{region_x}.{region_z}.mca"))

                for chunk in region.iter_chunks():
                    try:
                        for tile_entity in chunk["Level"]["TileEntities"]:
                            if "Items" in tile_entity and x1 <= tile_entity["x"].value <= x2 and y1 <= tile_entity[
                                "y"].value <= y2 and z1 <= tile_entity["z"].value <= z2:
                                items = self.get_items_from_nbt(tile_entity, items)

                    except KeyError:
                        continue

        self.cache[name] = {
            "last_update": time.time(),
            "items": items
        }

        return items

    def get_items_from_nbt(self, nbt, items):
        for item in nbt["Items"]:
            iid = item["id"][10:]
            if "shulker_box" in iid and "tag" in item:
                items = self.get_items_from_nbt(item["tag"]["BlockEntityTag"], items)

            else:
                count = item["Count"].value
                if iid not in items:
                    items[iid] = 0

                items[iid] += count

        return items
