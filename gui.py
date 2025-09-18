
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QScrollArea
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from characters import load_characters, add_character
from game import Game

def clear_layout(layout):
    """Рекурсивно видаляє всі віджети і під-layoutи"""
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clear_layout(child.layout())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Каталог персонажів та гра")
        self.resize(900, 600)

        self.characters = load_characters()
        self.selected_character = None
        self.game = Game()

        # Головний layout
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)

        # Ліва панель: персонажі + кнопки
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel, 1)

        # Прокручувана зона для персонажів
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.char_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.char_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.left_panel.addWidget(self.scroll_area)

        # Кнопки
        self.update_btn = QPushButton("Оновити каталог")
        self.update_btn.clicked.connect(self.update_characters)
        self.left_panel.addWidget(self.update_btn)

        self.add_btn = QPushButton("Додати персонажа")
        self.add_btn.clicked.connect(self.add_new_character)
        self.left_panel.addWidget(self.add_btn)

        self.attack_btn = QPushButton("Атакувати")
        self.attack_btn.clicked.connect(self.attack)
        self.left_panel.addWidget(self.attack_btn)

        self.save_btn = QPushButton("Зберегти гру")
        self.save_btn.clicked.connect(self.save_game)
        self.left_panel.addWidget(self.save_btn)

        self.load_btn = QPushButton("Завантажити гру")
        self.load_btn.clicked.connect(self.load_game)
        self.left_panel.addWidget(self.load_btn)

        # Права панель: текстова зона
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.main_layout.addWidget(self.text_area, 2)

        # Відобразити персонажів
        self.update_characters()

    def update_characters(self):
        clear_layout(self.char_layout)
        self.selected_character = None
        seen_names = set()

        for ch in self.characters:
            if ch.name in seen_names:
                continue
            seen_names.add(ch.name)

            hbox = QHBoxLayout()
            portrait_full_path = os.path.join(os.path.dirname(__file__), ch.portrait_path)

            pixmap = QPixmap()
            if not pixmap.load(portrait_full_path):
                pixmap = QPixmap(100, 100)  # порожній квадратик
            else:
                pixmap = pixmap.convertToFormat(QPixmap.Format.Format_ARGB32)
                pixmap = pixmap.scaled(100, 100,
                                       Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)

            label_img = QLabel()
            label_img.setPixmap(pixmap)
            label_img.setStyleSheet("border:1px solid gray; background-color:white;")

            label_name = QLabel(f"{ch.name}  HP:{ch.hp}  AP:{ch.ap}  Armor:{ch.armor}")
            label_name.setStyleSheet("font-weight: bold;")

            # Клік по картці обирає персонажа
            def select_char(event, c=ch):
                self.selected_character = c
                self.text_area.append(f"Обрано персонажа: {c.name}")

            label_img.mousePressEvent = select_char
            label_name.mousePressEvent = select_char

            hbox.addWidget(label_img)
            hbox.addWidget(label_name)
            self.char_layout.addLayout(hbox)

    def add_new_character(self):
        name, hp, ap, armor, path = "Новий", 100, 10, 5, "assets/portraits/Герой.jpg"
        add_character(name, hp, ap, armor, path)
        self.characters = load_characters()
        self.update_characters()
        self.text_area.append(f"Додано персонажа: {name}")

    def attack(self):
        if not self.selected_character:
            self.text_area.append("Виберіть персонажа для атаки!")
            return

        defender = None
        for ch in self.characters:
            if ch != self.selected_character:
                defender = ch
                break

        if not defender:
            self.text_area.append("Немає ворога для атаки!")
            return

        damage = self.game.attack(self.selected_character, defender)
        self.text_area.append(f"{self.selected_character.name} атакує {defender.name} на {damage} HP")
        self.text_area.append(f"{defender.name} зараз має {defender.hp} HP")

        if defender.hp == 0:
            self.text_area.append(f"{defender.name} повалений!")

    def save_game(self):
        self.text_area.append("Гра збережена (псевдозбереження).")

    def load_game(self):
        self.text_area.append("Гру завантажено (псевдозавантаження).")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
