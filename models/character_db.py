# models/character_db.py

from sqlalchemy import Column, Integer, String
from db.database import Base

class CharacterDB(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    house = Column(String, nullable=True)
    animal = Column(String, nullable=True)
    symbol = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    role = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    death = Column(Integer, nullable=True)
    strength = Column(String, nullable=True)
