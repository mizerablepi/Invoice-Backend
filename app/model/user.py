from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String
from .base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    firstname: Mapped[str] = mapped_column(String(20))
    lastname: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(20))
    username: Mapped[str] = mapped_column(String(20))
    password: Mapped[str]

class Key(Base):
    __tablename__ = "keys"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[int]


if __name__ == "__main__":
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///database.db",echo=True)

    with engine.begin() as con:
        Base.metadata.create_all(con)