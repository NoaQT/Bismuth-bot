import os
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from db.models import Server


async def add(interaction, name, path, db):
    if not os.path.exists(os.path.join(path, "server.properties")):
        return await interaction.response.send_message(f"server.properties not found in `{path}`")

    with Session(db) as session:
        res = session.scalars(select(Server)
            .where(or_(Server.name == name, Server.path == path))
        )
        if res.first():
            return await interaction.response.send_message("Server already exists")

        session.add(Server(name=name, path=path))
        session.commit()

    await interaction.response.send_message("Server added")


async def list(interaction, db):
    res = ""
    with Session(db) as session:
        for server in session.scalars(select(Server)):
            res += f"{server.name}\n"

    await interaction.response.send_message(res)
