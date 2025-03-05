import os
import discord

from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from db.models import Server
from commands.common import Pagination, MCQuery
from commands.common.server import get_or_default
from utils import parse_properties


async def add(interaction, name, path, hostname, db):
    if not os.path.exists(os.path.join(path, "server.properties")):
        return await interaction.response.send_message(f"server.properties not found in `{path}`")

    with Session(db) as session:
        res = session.scalars(select(Server)
            .where(or_(Server.name == name, Server.path == path, Server.hostname == hostname))
        )
        if res.first():
            return await interaction.response.send_message("Server already exists")

        default = session.scalars(select(Server).where(Server.default)).first()

        session.add(Server(name=name, path=path, hostname=hostname, default=default is None))
        session.commit()

    await interaction.response.send_message("Server added")


async def list(interaction, db):
    with Session(db) as session:
        servers = session.scalars(select(Server)).all()

    per_page = 5
    async def get_page(page):
        emb = discord.Embed(colour=0x9e42f5)
        emb.set_author(name="Servers", icon_url=interaction.guild.icon.url)

        servers_page = servers[(page - 1) * per_page:page * per_page]
        emb.add_field(name="Name", value="\n".join(s.name for s in servers_page), inline=True)
        emb.add_field(name="Host", value="\n".join(s.hostname for s in servers_page), inline=True)

        return emb

    return await Pagination(interaction, get_page, len(servers) // per_page + 1).view()


async def player_list(interaction, server_id, db):
    server = get_or_default(db, server_id)
    properties = parse_properties(os.path.join(server.path, "server.properties"))

    if not properties.get("enable-query", False):
        return await interaction.response.send_message("Query is not enable")

    query = MCQuery(port=int(properties.get("query-port", properties["server-port"])))
    try:
        res = await query.full_stat()
    except TimeoutError:
        return await interaction.response.send_message("Server is offline")

    players = res["players"]

    per_page = 10
    async def get_page(page):
        emb = discord.Embed(colour=0x9e42f5)
        emb.set_author(name=server.name, icon_url=interaction.guild.icon.url)
        players_page = players[(page - 1) * per_page:page * per_page]
        emb.add_field(
            name=f"{res['numplayers']}/{res['maxplayers']} players online:",
            value="\n" + "\n".join(p for p in players_page)
        )

        return emb

    return await Pagination(interaction, get_page, len(players) // per_page + 1).view()

