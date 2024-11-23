from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
import sys
from src.playing_chip import PlayingChip
from src.playing_card import PlayingCard
from src.playing_deck import PlayingDeck
from src.random_chips import RandomChips


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
        self.name_player.setStyleSheet("QLineEdit { "
                                       "color: black;"
                                       "border: none;"
                                        "background: transparent;"
                                        "}")
        self.name_player.setReadOnly(True)

        self.text = QLineEdit(self)
        self.text.setText(f'Фишки:{self.num_chips}')
        self.text.adjustSize()
        self.text.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.text.setFixedWidth(self.text.fontMetrics().horizontalAdvance(self.text.text()) + 10)
        self.text.setStyleSheet("QLineEdit { "
                                       "color: black;"
                                       "border: none;"
                                        "background: transparent;"
                                        "}")
        self.text.setReadOnly(True)

        self.layout_n_t.addWidget(self.name_player)
        self.layout_n_t.addWidget(self.text)

    def active_player(self):
        self.name_player.setStyleSheet("QLineEdit { "
                                       "color: red;"
                                       "border: none;"
                                        "background: transparent;"
                                        "}")
        
    def deactive_player(self):
        self.name_player.setStyleSheet("QLineEdit { "
                                       "color: black;"
                                       "border: none;"
                                        "background: transparent;"
                                        "}")

    def backlight(self, n):
        # Получаем виджеты из лейаута
        widgets = []
        while self.card_layout.count():
            widget_item = self.card_layout.takeAt(0)
            widget = widget_item.widget()
            if widget:
                widgets.append(widget)

        # Добавляем виджеты обратно в лейаут
        for card in widgets:
            if card.num == n:
                card.active_backlight()
            else:
                card.deactive_backlight()
            self.card_layout.addWidget(card)

    def sort_cards(self):
        # Получаем виджеты из лейаута
        widgets = []
        while self.card_layout.count():
            widget_item = self.card_layout.takeAt(0)
            widget = widget_item.widget()
            if widget:
                widgets.append(widget)

        # Сортируем виджеты по num
        widgets.sort(key=lambda card: card.num)

        # Добавляем виджеты обратно в лейаут
        for card in widgets:
            self.card_layout.addWidget(card)
    
    def score_num_card(self):
        score = 0
        num_list = []
        while self.card_layout.count():
            widget_item = self.card_layout.takeAt(0)
            widget = widget_item.widget()
            if widget:
                try:
                    num_list.append(int(widget.num))
                except (ValueError):
                    pass  # Если num отсутствует, ничего не прибавляем
        for i in num_list:
            if (i - 1) in num_list:
                continue
            else:
                score += i
        return score

    def add_card(self, n):
        new_card = PlayingCard(num=n, size=(44, 66))
        self.card_layout.addWidget(new_card)
        return new_card
    

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
