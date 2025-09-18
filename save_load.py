import json
import os

SAVE_DIR = "saves/"

def save_game(game, filename="save.json"):
    os.makedirs(SAVE_DIR, exist_ok=True)
    data = {
        "player": vars(game.player),
        "enemy": vars(game.enemy),
        "history": game.history
    }
    with open(os.path.join(SAVE_DIR, filename), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_game(filename="save.json"):
    path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    from game import Character, Game
    player = Character(**data["player"])
    enemy = Character(**data["enemy"])
    game = Game(player, enemy)
    game.history = data["history"]
    return game
