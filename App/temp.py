# from model imp
from model.base import Base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.db")

Base.metadata.create_all(engine)