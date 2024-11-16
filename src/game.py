from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLineEdit, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont
import random
import sys
from src.playing_chip import PlayingChip
from src.playing_card import PlayingCard
from src.playing_deck import PlayingDeck
from src.random_chips import RandomChips
from src.player import Player
from src.adjustment_start_game import NUMBER_PLAYERS, NAME_PLAYERS
from src.highlighted_playing_card import PlayingHighlightedCard
NAME_PLAYERS = ['Игрок №1', 'Игрок №22222222', 'Игрок №3', 'Игрок №4']
NUMBER_PLAYERS = 4


class Game(QWidget):
    def __init__(self, parent=None, num_players=3):
        super().__init__(parent)

        self.deck = list(random.sample(range(3, 36), 24))
        self.players = []
        self.num_current_player = 0

        # Главный вертикальный лейаут
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 5)

        self.top_layout = QHBoxLayout()

        self.deck_card = PlayingDeck(self, num=24, size=(120, 180))
        self.top_layout.addWidget(self.deck_card)

        self.card = PlayingCard(self, num='', size=(120, 180))
        self.top_layout.addWidget(self.card)

        self.chip = PlayingChip(self, size=180)
        self.top_layout.addWidget(self.chip)

        self.main_layout.addLayout(self.top_layout)
        # self.main_layout.addLayout(self.annotation)
        self.main_layout.addStretch()

        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.main_layout.addWidget(self.line)

        for i in range(NUMBER_PLAYERS):
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)

            player = Player(self, NAME_PLAYERS[i], 0)
            # player.add_chips(10)
            self.players.append(player)
            self.main_layout.addWidget(player)
            self.main_layout.addWidget(line)
        
        self.who_move = QLineEdit(self)
        self.who_move.setText(f'-> Нажмите для раздачи фишек ->')
        self.who_move.adjustSize()
        self.who_move.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.who_move.setFixedWidth(self.who_move.fontMetrics().horizontalAdvance(self.who_move.text()) + 10)
        self.who_move.setStyleSheet("QLineEdit { border: none; background: transparent; }")
        self.who_move.setReadOnly(True)

        self.bottom_layout = QHBoxLayout()

        self.bottom_layout.addWidget(self.who_move)

        self.button_give_chips = QPushButton(self)
        self.button_give_chips.setText('Раздать фишки')
        self.button_give_chips.clicked.connect(self.give_chips)
        self.bottom_layout.addWidget(self.button_give_chips)

        self.button_start_game = QPushButton(self)
        self.button_start_game.setText('Начать игру')
        self.bottom_layout.addWidget(self.button_start_game)
        self.button_start_game.clicked.connect(self.start_game)
        self.button_start_game.hide()

        self.button_pay_off = QPushButton(self)
        self.button_pay_off.setText('Откупиться')
        self.bottom_layout.addWidget(self.button_pay_off)
        self.button_pay_off.clicked.connect(self.pay_off)
        self.button_pay_off.hide()

        self.button_take_card = QPushButton(self)
        self.button_take_card.setText('Взять карту')
        self.bottom_layout.addWidget(self.button_take_card)
        self.button_take_card.clicked.connect(self.take_card)
        self.button_take_card.hide()

        self.main_layout.addLayout(self.bottom_layout)

    def start_game(self):
        self.button_start_game.hide()
        self.button_pay_off.show()
        self.button_take_card.show()
        self.who_move.setText(f'-> Ход игрока: {NAME_PLAYERS[self.num_current_player]}')

        self.card.update_num(self.deck[-1])
        self.deck_card.update_num(self.deck_card.num - 1)
    
    def pay_off(self):
        pass

    def take_card(self):
        pass

    def give_chips(self):
        # print("Раздача фишек начата")
        if 3 <= NUMBER_PLAYERS <= 5:
            for i in range(NUMBER_PLAYERS):
                print(i, self.players[i].name)
                self.players[i].add_chips(11)
                # self.players[i].show()
        elif NUMBER_PLAYERS == 6:
            for i in range(NUMBER_PLAYERS):
                self.players[i].add_chips(9)
        elif NUMBER_PLAYERS == 7:
            for i in range(NUMBER_PLAYERS):
                self.players[i].add_chips(7)

        self.who_move.setText('-> Нажмите для начала игры ->')
        self.button_give_chips.hide()
        self.button_start_game.show()



    def paintEvent(self, event):
        super().paintEvent(event)
        
        # Создаем объект для рисования
        painter = QPainter(self)
        
        # Устанавливаем цвет и другие параметры рисования для прямоугольника
        painter.setPen(QColor(0, 0, 0, 100))  # Полупрозрачный цвет для рамки
        painter.setBrush(QColor(0, 0, 0, 50))  # Полупрозрачная заливка
        
        # Получаем размер области для рисования
        rect = self.rect()
        
        # Рассчитываем вертикальное положение прямоугольника
        y_position_rect = rect.bottom() - 472  # Верхний край прямоугольника 470 пикселей от нижнего края
        
        # Устанавливаем размеры прямоугольника (ширина - вся ширина окна, высота - 470 пикселей)
        rectangle_width = rect.width()
        rectangle_height = 472  # Высота прямоугольника

        # Создаем прямоугольник для рисования
        rect_to_draw = QRect(0, y_position_rect, rectangle_width, rectangle_height)
        
        # Рисуем прямоугольник
        painter.drawRect(rect_to_draw)
        
        # Устанавливаем шрифт и цвет текста
        painter.setFont(QFont("Arial", 12))
        painter.setPen(QColor(0, 0, 0, 100))  # Полупрозрачный цвет для текста
        
        # Рассчитываем y-координату для текста
        y_position_text = rect.top() + 210  # Текст не ниже 210 пикселей от верхней границы
        
        # Рассчитываем x-координаты для текстов
        x_position_text_center = rect.center().x()  # Центр
        x_position_text_left = int((rect.width() -20 - 420) * (210 / 840)) + 25 # Сдвиг на 200 пикселей влево от центра
        x_position_text_right = int((rect.width() -20 - 420) * (630 / 840)) + 285  # Сдвиг на 150 пикселей вправо от центра
        
        # Определяем области для рисования текстов
        text_rect_left = QRect(x_position_text_left, y_position_text, rect.width() - x_position_text_left, rect.bottom() - y_position_text - rectangle_height)
        text_rect_right = QRect(x_position_text_right, y_position_text, rect.width() - x_position_text_right, rect.bottom() - y_position_text - rectangle_height)
        text_rect_center = QRect(x_position_text_center - 70, y_position_text, rect.width() - (x_position_text_center - 70), rect.bottom() - y_position_text - rectangle_height)
        
        # Рисуем первый текст (сдвинутый влево)
        painter.drawText(text_rect_left, Qt.AlignmentFlag.AlignTop, "Количество карт\n      в колоде") #"  Количество\nкарт в колоде"
        
        # Рисуем второй текст (сдвинутый вправо)
        painter.drawText(text_rect_right, Qt.AlignmentFlag.AlignTop, "Количество фишек \n         на карте")
        
        # Рисуем основной текст (по центру)
        painter.drawText(text_rect_center, Qt.AlignmentFlag.AlignTop, "Текущая карта")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Game(num_players=5)
    window.show()
    sys.exit(app.exec())


# Писать чей ход в баре