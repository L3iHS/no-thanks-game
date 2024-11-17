from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLineEdit, QSizePolicy, QLabel
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont
import random
import sys
from src.playing_chip import PlayingChip
from src.playing_card import PlayingCard
from src.playing_deck import PlayingDeck
from src.random_chips import RandomChips
from src.table_with_results import TableWithResults
from src.player import Player
from src.config import Config
from src.highlighted_playing_card import PlayingHighlightedCard
# NAME_PLAYERS = ['Игрок №1', 'Игрок №22222222', 'Игрок №3', 'Игрок №4', 'plyaer №5']
# NUMBER_PLAYERS = 4

#  доделать подсчет очков карт идущих подряд


class Game(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        print(Config.NUMBER_PLAYERS, Config.NAME_PLAYERS)

        self.deck = list(random.sample(range(3, 36), 24))
        self.players = []
        self.num_current_player = 0
        self.last_player = ''
        # self.last_card = PlayingCard(self, num='', size=(120, 180))

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

        for i in range(Config.NUMBER_PLAYERS):   # for i in range(Config.NUMBER_PLAYERS):
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)

            player = Player(self, Config.NAME_PLAYERS[i], 0)  # player = Player(self, Config.NAME_PLAYERS[i], 0)
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

        self.button_count_points = QPushButton(self)
        self.button_count_points.setText('Подсчитать очки')
        self.bottom_layout.addWidget(self.button_count_points)
        self.button_count_points.clicked.connect(self.count_points)
        self.button_count_points.hide()
        self.card.card_cleared.connect(self.on_card_cleared)

        self.button_print_result = QPushButton(self)
        self.button_print_result.setText('Вывести результат')
        self.bottom_layout.addWidget(self.button_print_result)
        self.button_print_result.clicked.connect(self.print_result)
        self.button_print_result.hide()

        self.main_layout.addLayout(self.bottom_layout)

    def start_game(self):
        self.button_start_game.hide()
        self.button_pay_off.show()
        if self.players[self.num_current_player].num_chips <= 0:
            self.button_pay_off.setDisabled(True)
        else:
            self.button_pay_off.setDisabled(False)
        self.button_take_card.show()
        self.who_move.setText(f'-> Ход игрока: {Config.NAME_PLAYERS[self.num_current_player]}')
        self.players[self.num_current_player].active_player()

        self.card.update_num(self.deck.pop(-1)) # Достаем карту из колоды и кладем на стол
        self.deck_card.update_num(self.deck_card.num - 1)

    def on_card_cleared(self):
        self.button_pay_off.hide()
        self.button_take_card.hide()
        self.players[self.num_current_player].deactive_player()
        self.players[self.num_current_player].backlight('')
        self.who_move.setText('-> Подсчитать очки ->')

        self.button_count_points.show()

    def print_result(self):
        self.table.output_results()
        for i in range(Config.NUMBER_PLAYERS):
            # print(f'{Config.NAME_PLAYERS[i]}, набравший {places_and_score[i][1]}б , занимает {places_and_score[i][0]} место')
            place, name, score = self.table.print_result(self.date, Config.NAME_PLAYERS[i])
            print(f'{name}, набравший {score}б , занимает {place} место')
        self.table.show()
        
    def count_points(self): #########################################
        self.table = TableWithResults()
        for i in range(Config.NUMBER_PLAYERS):
            score_card = self.players[i].score_num_card()
            score_chips = self.players[i].num_chips
            score = score_card - score_chips
            place, self.date = self.table.add_player(Config.NAME_PLAYERS[i], score) # Добовляем результат игрока в базу данных
        
        self.button_count_points.hide()
        self.who_move.setText('-> Вывести результат ->')
        self.button_print_result.show()
        
        

    def pay_off(self): # Откупиться
        # self.button_pay_off.setDisabled(False)
        self.players[self.num_current_player].add_chips(-1)
        self.chip.add_chips(1)

        self.num_current_player += 1
        self.num_current_player %= Config.NUMBER_PLAYERS
        self.who_move.setText(f'-> Ход игрока: {Config.NAME_PLAYERS[self.num_current_player]}')
        if self.players[self.num_current_player].num_chips <= 0:
            self.button_pay_off.setDisabled(True)
        else:
            self.button_pay_off.setDisabled(False)

        self.players[self.num_current_player - 1].deactive_player()
        self.players[self.num_current_player].active_player()

    def take_card(self): # Взять карту
        self.players[self.num_current_player].add_chips(self.chip.reset_to_zero())
        self.button_pay_off.setDisabled(False)

        self.players[self.num_current_player].add_card(self.card.num)

        if self.last_player != '':
            self.players[self.last_player].backlight(self.card.num)

        self.last_player = self.num_current_player
        self.players[self.num_current_player].sort_cards()
        self.players[self.num_current_player].backlight(self.card.num)

        if len(self.deck) > 0:
            self.card.update_num(self.deck.pop(-1))
            self.deck_card.update_num(self.deck_card.num - 1)
        else:
            self.card.update_num('')

    def give_chips(self):
        # print("Раздача фишек начата")
        if 3 <= Config.NUMBER_PLAYERS <= 5:
            for i in range(Config.NUMBER_PLAYERS):
                print(i, self.players[i].name)
                self.players[i].add_chips(11)
                # self.players[i].show()
        elif Config.NUMBER_PLAYERS == 6:
            for i in range(Config.NUMBER_PLAYERS):
                self.players[i].add_chips(9)
        elif Config.NUMBER_PLAYERS == 7:
            for i in range(Config.NUMBER_PLAYERS):
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
        y_height_rectangle = 51 + 105 * Config.NUMBER_PLAYERS # Высота прямоугольника
        
        # Рассчитываем вертикальное положение прямоугольника
        y_position_rect = rect.bottom() - y_height_rectangle  # Верхний край прямоугольника 470 пикселей от нижнего края
        
        # Устанавливаем размеры прямоугольника (ширина - вся ширина окна, высота - 470 пикселей)
        rectangle_width = rect.width()
        rectangle_height = y_height_rectangle + 1  # Высота прямоугольника

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
    window = Game()
    window.show()
    sys.exit(app.exec())