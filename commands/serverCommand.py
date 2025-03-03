import os
import discord

from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from db.models import Server
from .common import Pagination
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

