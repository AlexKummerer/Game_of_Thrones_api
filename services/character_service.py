from typing import List, Optional
from sqlalchemy.orm import Session
from models.character import Character
from models.character_db import CharacterDB
from db.database import SessionLocal
import random


class CharacterService:

    def __init__(self, characters: List[Character]):
        self.db: Session = SessionLocal()

    def get_all_characters(
        self,
        limit: int = 20,
        skip: int = 0,
        filters: Optional[dict] = None,
        sort_asc: Optional[str] = None,
        sort_desc: Optional[str] = None,
    ) -> List[Character]:
        """
        This method retrieves a list of characters from the character service.
        It allows for pagination by specifying a limit and a skip value.
        The limit determines the maximum number of characters to return,
        while the skip value determines how many characters to skip from the start.
        If both limit and skip are set to 0, it returns a random sample of characters.

        Args:
            limit (int): The maximum number of characters to return.
            skip (int): The number of characters to skip.
        Returns:
            List[Character]: A list of characters.
        """
        query = self.db.query(CharacterDB)

        if filters:
            if filters.get("name"):
                query = query.filter(CharacterDB.name.ilike(f"%{filters['name']}%"))
            if filters.get("house"):
                query = query.filter(CharacterDB.house.ilike(f"%{filters['house']}%"))
            if filters.get("role"):
                query = query.filter(CharacterDB.role.ilike(f"%{filters['role']}%"))
            if filters.get("age") is not None:
                query = query.filter(CharacterDB.age == filters["age"])
            if filters.get("age_more_than") is not None:
                query = query.filter(CharacterDB.age >= filters["age_more_than"])
            if filters.get("age_less_than") is not None:
                query = query.filter(CharacterDB.age <= filters["age_less_than"])


        if sort_asc:
            try:
                query = query.order_by(getattr(CharacterDB, sort_asc).asc())
            except AttributeError:
                raise ValueError(f"Cannot sort ascending by '{sort_asc}'")
        if sort_desc:
            try:
                query = query.order_by(getattr(CharacterDB, sort_desc).desc())
            except AttributeError:
                raise ValueError(f"Cannot sort descending by '{sort_desc}'")


    # Pagination
        if limit == 0:
            characters = query.all()
            return random.sample(characters, min(20, len(characters)))
        else:
            characters = query.offset(skip).limit(limit).all()
            return characters

    def get_character_by_id(self, character_id: int) -> Character:
        """
        This method retrieves a character by its ID.

        Args:
            character_id (int): The ID of the character to retrieve.
        Returns:
            Character: The character with the specified ID.
        """
        return self.db.query(CharacterDB).filter(CharacterDB.id == character_id).first()


    def add_character(self, character_data: dict) -> Character:
        """
        This method adds a new character to the character service.

        Args:
            character_data (dict): The data of the character to add.
        Returns:
            Character: The newly added character.
        """
        new_character = CharacterDB(**character_data)
    
        self.db.add(new_character)
        self.db.commit()
        self.db.refresh(new_character)
        print(new_character.name)
        return new_character

    def update_character(self, character_id: int, updated_data: dict) -> Character:
        """
        This method updates an existing character in the character service.

        Args:
            character_id (int): The ID of the character to update.
            updated_data (dict): The updated data for the character.
        Returns:
            Character: The updated character.
        """
        character = self.get_character_by_id(character_id)
        if character:
            for key, value in updated_data.items():
                if hasattr(character, key):
                    setattr(character, key, value)
                self.db.commit()
                self.db.refresh(character)
            return character
        return None

    def delete_character(self, character_id: int) -> bool:
        """
        Deletes an existing character

        Args:
            character_id (int): The id of the character to delete

        Returns:
            bool:  True if successful deleted, if not False
        """
        character = self.get_character_by_id(character_id)
        if character:
            self.db.delete(character)
            self.db.commit()            
            return True
        return False

    def get_character_by_name(self, name: str) -> Optional[CharacterDB]:
        return self.db.query(CharacterDB).filter(CharacterDB.name.ilike(name)).first()
