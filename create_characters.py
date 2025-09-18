from characters import add_character

characters_info = [
    ("Герой", 120, 20, 10, "assets/portraits/Герой.png"),
    ("Ворог", 100, 15, 5, "assets/portraits/Ворог.png"),
    ("Маг", 90, 25, 5, "assets/portraits/Маг.png"),
    ("Лучник", 110, 18, 8, "assets/portraits/Лучник.png"),
    ("Рицар", 130, 15, 12, "assets/portraits/Рицар.png")
]

for name, hp, ap, armor, path in characters_info:
    add_character(name, hp, ap, armor, path)

print("5 тестових персонажів створено.")
