
import json
import os
from utils import download_image

CHARACTERS_FILE = os.path.join("assets", "characters.json")

class CharacterData:
    def __init__(self, name, hp, ap, armor, portrait_path):
        self.name = name
        self.hp = hp
        self.ap = ap
        self.armor = armor
        self.portrait_path = portrait_path  # Локальний шлях до портрета

def load_characters():
    if not os.path.exists(CHARACTERS_FILE):
        return []
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    chars = []
    for c in data:
        chars.append(CharacterData(
            c["name"], c["hp"], c["ap"], c["armor"], c["portrait_path"]
        ))
    return chars

def save_characters(characters):
    data = []
    for c in characters:
        data.append({
            "name": c.name,
            "hp": c.hp,
            "ap": c.ap,
            "armor": c.armor,
            "portrait_path": c.portrait_path
        })
    if not os.path.exists("assets"):
        os.makedirs("assets")
    with open(CHARACTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_character(name, hp, ap, armor, portrait_path):
    characters = load_characters()
    new_char = CharacterData(name, hp, ap, armor, portrait_path)
    characters.append(new_char)
    save_characters(characters)
