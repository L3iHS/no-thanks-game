import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QLineEdit, QPushButton, QSpinBox
from PyQt6.QtCore import pyqtSignal
from data.playing_chip import PlayingChip
from data.playing_card import PlayingCard


NUMBER_PLAYERS = 3
NAME_PLAYERS = []


class Adjustment_Start_Game(QMainWindow):
    start_button_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
    
    def initUI(self):
        self.setGeometry(600, 300, 370, 50)
        self.setWindowTitle('Настройка игры')

        self.players = []

        self.text1 = QLineEdit(self)
        self.text1.setText('Выберите количество игроков:')
        self.text1.resize(200, 20)
        self.text1.move(10, 20)
        self.text1.setReadOnly(True)
        self.text1.setStyleSheet("QLineEdit { border: none; background: transparent; }")
        # 220

        self.number_players = QSpinBox(self)
        self.number_players.resize(40, 20)
        self.number_players.move(220, 20)
        self.number_players.setRange(3, 7)
        self.number_players.setValue(3)
        self.number_players.lineEdit().setReadOnly(True)

        self.button_apply1 = QPushButton(self)
        self.button_apply1.setText('Применить')
        self.button_apply1.resize(90, 30)
        self.button_apply1.move(270, 15)
        self.button_apply1.clicked.connect(self.apply_1)
        self.button_apply1.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                border: 1px solid #ccc;
            }
        """)

        self.button_apply2 = QPushButton(self)
        self.button_apply2.setText('Применить')
        self.button_apply2.resize(90, 30)
        self.button_apply2.clicked.connect(self.apply_2)
        self.button_apply2.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                border: 1px solid #ccc;
            }
        """)
        self.button_apply2.hide()

    def apply_1(self):
        x_start = 10
        y_start = 40
        self.resize(self.width(), 50 + int(self.number_players.text()) * 30 + 20)
        NAME_PLAYERS = []
        
        for i in range(1, int(self.number_players.text()) + 1):
            text = QLineEdit(self)
            text.setText(f'Игрок №{i}')
            text.resize(70, 20)
            text.move(x_start, y_start + i * 30)
            text.setReadOnly(True)
            text.setStyleSheet("QLineEdit { border: none; background: transparent; }")
            text.show()

            input_text = QLineEdit(self)
            input_text.setText(f'Игрок №{i}')
            input_text.resize(70, 20)
            input_text.move(x_start + 90, y_start  + i * 30)
            input_text.show()

            self.players.append(input_text)
        
        self.button_apply1.hide()
        self.button_apply2.move(self.width() - 100, self.height() - 40)
        self.button_apply2.show()
    
    def apply_2(self):
        NUMBER_PLAYERS = int(self.number_players.text())
        
        for i in range(NUMBER_PLAYERS):
            NAME_PLAYERS.append(self.players[i].text())
        # создать базу данных с именами игроков
        self.start_button_signal.emit()
        print(NAME_PLAYERS)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Adjustment_Start_Game()
    ex.show()
    sys.exit(app.exec())
