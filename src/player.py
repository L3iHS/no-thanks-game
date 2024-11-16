from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
import sys
from src.playing_chip import PlayingChip
from src.playing_card import PlayingCard
from src.playing_deck import PlayingDeck
from src.random_chips import RandomChips
from src.adjustment_start_game import NUMBER_PLAYERS, NAME_PLAYERS
from src.highlighted_playing_card import PlayingHighlightedCard
NAME_PLAYERS = ['Игрок №1', 'Игрок №22222222', 'Игрок №3', 'Игрок №4']
NUMBER_PLAYERS = 0


class Player(QWidget):
    def __init__(self, parent, name, num_chips):
        super().__init__(parent)
        
        self.setFixedHeight(80)

        self.name = name
        self.num_chips = num_chips

        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.setContentsMargins(5, 5, 5, 5)

        
        self.layout_n_t = QVBoxLayout()
        self.main_layout.addLayout(self.layout_n_t)
        # self.layout_n_t.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.chips = RandomChips(self, 69, 69, 20, self.num_chips)
        self.chips.setFixedSize(70, 70)
        self.main_layout.addWidget(self.chips)

        self.card_layout = QHBoxLayout()
        self.main_layout.addLayout(self.card_layout)
        

        self.name_player = QLineEdit(self)
        self.name_player.setText(self.name)
        self.name_player.adjustSize()
        self.name_player.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.name_player.setFixedWidth(self.name_player.fontMetrics().horizontalAdvance(self.name_player.text()) + 10)
        self.name_player.setStyleSheet("QLineEdit { border: none; background: transparent; }")
        self.name_player.setReadOnly(True)

        self.text = QLineEdit(self)
        self.text.setText(f'Фишки:{self.num_chips}')
        self.text.adjustSize()
        self.text.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.text.setFixedWidth(self.text.fontMetrics().horizontalAdvance(self.text.text()) + 10)
        self.text.setStyleSheet("QLineEdit { border: none; background: transparent; }")
        self.text.setReadOnly(True)

        self.layout_n_t.addWidget(self.name_player)
        self.layout_n_t.addWidget(self.text)

    def add_card(self, n):
        self.card_layout.addWidget(PlayingCard(num=n, size=(44, 66)))

    def add_chips(self, n):
        self.num_chips += n
        self.text.setText(f'Фишки:{self.num_chips}')
        # print(f'Игрок: {self.name}, Фишек добавлено: {n}, Всего фишек: {self.num_chips}')  # Отладочная информация

        # print(self.num_chips)
        self.chips.generating_chips(self.num_chips)
        self.chips.show()
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Player(None, 'Игрок №111111', 4)
    window.add_card(6)
    window.add_chips(2)
    window.show()
    sys.exit(app.exec())
