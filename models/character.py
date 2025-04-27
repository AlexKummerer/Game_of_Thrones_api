class Character:
    def __init__(self, id, name, house, animal, symbol, nickname, role, age, death, strength):
        self.id = id
        self.name = name
        self.house = house
        self.animal = animal
        self.symbol = symbol
        self.nickname = nickname
        self.role = role
        self.age = age
        self.death = death
        self.strength = strength

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "house": self.house,
            "animal": self.animal,
            "symbol": self.symbol,
            "nickname": self.nickname,
            "role": self.role,
            "age": self.age,
            "death": self.death,
            "strength": self.strength,
        }
