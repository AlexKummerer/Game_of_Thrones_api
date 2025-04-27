import json
from models.character import Character

def load_characters_from_json(filepath):
    characters = []
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for char in data:
            character = Character(
                id=char.get('id'),
                name=char.get('name'),
                house=char.get('house'),
                animal=char.get('animal'),
                symbol=char.get('symbol'),
                nickname=char.get('nickname'),
                role=char.get('role'),
                age=char.get('age'),
                death=char.get('death'),
                strength=char.get('strength')
            )
            characters.append(character)
    return characters