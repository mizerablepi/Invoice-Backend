from sqlalchemy import create_engine, insert
from app.model.user import Key
import random

engine = create_engine("sqlite:///database.db")

key = random.randint(0,10000)

with engine.begin() as con:
    con.execute(insert(Key).values(key=key))
    con.commit()