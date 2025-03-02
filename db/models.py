from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    path: Mapped[str] = mapped_column(unique=True)
    default: Mapped[bool] = mapped_column(default=False)
