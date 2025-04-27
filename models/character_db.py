# models/character_db.py

from sqlalchemy import Column, Integer, String
from db.database import Base

class CharacterDB(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    house = Column(String, nullable=False)
    animal = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    role = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    death = Column(Integer, nullable=True)
    strength = Column(String, nullable=True)
