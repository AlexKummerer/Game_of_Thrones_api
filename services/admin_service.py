import os
from services.data_loader import load_characters_from_json
from models.character_db import CharacterDB
from db.database import SessionLocal


class AdminService:
    @staticmethod
    def load_json_into_db():
        session = SessionLocal()
        characters_filepath = os.path.join("data", "characters.json")
        characters_data = load_characters_from_json(characters_filepath)

        for character in characters_data:

            existing_character = (
                session.query(CharacterDB).filter_by(name=character.name).first()
            )
            if existing_character:
                continue

            db_character = CharacterDB(
                name=character.name,
                house=character.house,
                animal=character.animal,
                symbol=character.symbol,
                nickname=character.nickname,
                role=character.role,
                age=character.age,
                death=character.death,
                strength=character.strength,
            )
            session.add(db_character)

        session.commit()
        session.close()
