import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.screen_ui.start_screen import Ui_MainWindow
from src.adjustment_start_game import Adjustment_Start_Game, NAME_PLAYERS, NUMBER_PLAYERS
from src.game import Game


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.rules_button.clicked.connect(self.open_pdf)

        self.exit_button.clicked.connect(self.close_app)

        self.setting_button.clicked.connect(self.setting_game)

        self.start_button.clicked.connect(self.start_game)
        self.start_button.hide()
    
    def open_rules(self):
        pass
    
    def close_app(self):
        self.close()
    
    def setting_game(self):
        self.setting = Adjustment_Start_Game()  # Создаем экземпляр экрана настройки игры
        self.setting.start_button_signal.connect(self.show_start_button)
        self.setting.show()
        # if self.setting:
        #     print('okey')
        #     self.start_button.show()
    
    def show_start_button(self):
        self.start_button.show()
        self.setting_button.hide()

    def start_game(self):
        self.game = Game(NUMBER_PLAYERS)
        self.game.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())

