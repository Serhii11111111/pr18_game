from characters import CharacterData, load_characters, save_characters

class Game:
    def __init__(self):
        self.characters = load_characters()
        self.history = []

    def attack(self, attacker: CharacterData, defender: CharacterData):
        damage = max(attacker.ap - defender.armor, 0)
        defender.hp -= damage
        self.history.append(f"{attacker.name} атакує {defender.name} на {damage} HP")
        if defender.hp <= 0:
            defender.hp = 0
            self.history.append(f"{defender.name} повалений!")
        save_characters(self.characters)
        return damage
