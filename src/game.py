from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
import sys
from data.playing_chip import PlayingChip
from data.playing_card import PlayingCard
from data.playing_deck import PlayingDeck
from src.adjustment_start_game import NUMBER_PLAYERS, NAME_PLAYERS
from data.highlighted_playing_card import PlayingHighlightedCard
NAME_PLAYERS = ['Игрок №1', 'Игрок №22222222', 'Игрок №3']


class Game(QWidget):
    def __init__(self, num_players=3, parent=None):
        super().__init__(parent)

        # Главный вертикальный лейаут
        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        card = PlayingDeck(self, 47, (120, 180))
        top_layout.addWidget(card)
        card = PlayingHighlightedCard(self, 2, (120, 180))
        top_layout.addWidget(card)
        chip = PlayingChip(self, size=180)
        top_layout.addWidget(chip)
        # card = PlayingCard(self, 3, (120, 180))
        # top_layout.addWidget(card)

        main_layout.addLayout(top_layout)
        main_layout.addStretch()

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Список для хранения лейаутов
        self.layouts = {}

        # Создаем несколько лейаутов в цикле
        for i in range(1, num_players + 1):
            # Создаем новый горизонтальный лейаут для каждой итерации
            layout = QHBoxLayout()
            layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            layout_t = QVBoxLayout()

            name = QLineEdit(self)
            name.setText(NAME_PLAYERS[i - 1])
            name.adjustSize()
            name.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            name.setFixedWidth(name.fontMetrics().horizontalAdvance(name.text()) + 10)
            name.setStyleSheet("QLineEdit { border: none; background: transparent; }")
            name.setReadOnly(True)
            
            text = QLineEdit(self)
            text.setText(NAME_PLAYERS[i - 1])
            text.adjustSize()
            text.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            text.setFixedWidth(text.fontMetrics().horizontalAdvance(text.text()) + 10)

            

            layout_t.addWidget(name)
            layout_t.addWidget(text)
            layout.addLayout(layout_t)

            chips_count = 0

            main_layout.addLayout(layout)
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            main_layout.addWidget(line)

            # Сохраняем лейаут в список
            self.layouts[str(i)] = layout

        self.setLayout(main_layout)
        self.show()

        card = PlayingCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)
        card = PlayingCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)
        card = PlayingCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)
        card = PlayingCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)
        card = PlayingCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)
        card = PlayingHighlightedCard(self, 47, (44, 66))
        self.layouts['1'].addWidget(card)

        chip = PlayingChip(self, size=66)
        self.layouts['2'].addWidget(chip)
        # top_layout.addWidget(chip)
        card = PlayingCard(self, 34, (44, 66))
        self.layouts['2'].addWidget(card)

        card = PlayingCard(self, 51, (44, 66))
        self.layouts['2'].addWidget(card)

        card = PlayingCard(self, 23, (44, 66))
        self.layouts['3'].addWidget(card)

        # card = PlayingCard(self, 25, (44, 66))
        # self.layouts['4'].addWidget(card)

        # card = PlayingCard(self, 41, (44, 66))
        # self.layouts['5'].addWidget(card)

        # card = PlayingCard(self, 32, (44, 66))
        # self.layouts['6'].addWidget(card)

        # card = PlayingCard(self, 6, (44, 66))
        # self.layouts['7'].addWidget(card)

        # card = PlayingCard(self, 51, (44, 66))
        # self.layouts['7'].addWidget(card)

        # card = PlayingCard(self, 17, (44, 66))
        # self.layouts['7'].addWidget(card)

        # Доступ к лейауту по индексу и изменение текста на кнопке
        # layout = self.layouts[0]
        # Пример: изменить текст первой кнопки в лейауте
        # layout.itemAt(0).widget().setText('new_text')

if __name__ == '__main__':
    app = QApplication([])
    window = Game()
    sys.exit(app.exec())


# Писать чей ход в баре