import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import Server
from nbt import nbt

def get_or_default(db_engine, server_id):
    with (Session(db_engine) as session):
        return session.scalars(select(Server).where(Server.id == server_id)).first() \
            or session.scalars(select(Server).where(Server.default)).first()


def world_path(server):
    return os.path.join(str(server.path), "bismuth_smp")

def scoreboard_nbt(server):
    return nbt.NBTFile(os.path.join(world_path(server), "data", "scoreboard.dat"))