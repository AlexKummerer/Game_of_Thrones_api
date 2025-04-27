from typing import List, Optional
from models.character import Character
import random


class CharacterService:

    def __init__(self, characters: List[Character]):
        self.characters = characters

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
        result = self.characters

        if filters:
            if filters.get("name"):
                result = [
                    char
                    for char in result
                    if filters["name"].lower() in (char.name or "").lower()
                ]
            if filters.get("house"):
                result = [
                    char
                    for char in result
                    if filters["house"].lower() in (char.house or "").lower()
                ]
            if filters.get("role"):
                result = [
                    char
                    for char in result
                    if filters["role"].lower() in (char.role or "").lower()
                ]
            if filters.get("age") is not None:
                result = [char for char in result if char.age == filters["age"]]
            if filters.get("age_more_than") is not None:
                result = [
                    char
                    for char in result
                    if char.age is not None and char.age >= filters["age_more_than"]
                ]
            if filters.get("age_less_than") is not None:
                result = [
                    char
                    for char in result
                    if char.age is not None and char.age <= filters["age_less_than"]
                ]

        if sort_asc:
            try:
                result = sorted(result, key=lambda x: getattr(x, sort_asc))
            except ArithmeticError:
                raise ValueError(f"Cannot sort ascending by '{sort_asc}")

        if sort_desc:
            try:
                result = sorted(
                    result, key=lambda x: getattr(x, sort_desc), reverse=True
                )
            except AttributeError:
                raise ValueError(f"Cannot sort descending by '{sort_desc}")

        if limit == 0:
            result = random.sample(result, min(20, len(result)))
        else:
            if skip >= len(result):
                result = []
            result = result[skip : skip + limit]

        return result

    def get_character_by_id(self, character_id: int) -> Character:
        """
        This method retrieves a character by its ID.

        Args:
            character_id (int): The ID of the character to retrieve.
        Returns:
            Character: The character with the specified ID.
        """
        return next((char for char in self.characters if char.id == character_id), None)

    def add_character(self, character_data: dict) -> Character:
        """
        This method adds a new character to the character service.

        Args:
            character_data (dict): The data of the character to add.
        Returns:
            Character: The newly added character.
        """
        new_id = max((char.id for char in self.characters), default=0) + 1
        character_data["id"] = new_id
        new_character = Character(**character_data)
        self.characters.append(new_character)
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
            self.characters.remove(character)
            return True
        return False
