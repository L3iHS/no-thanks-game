import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.screen_ui.start_screen import Ui_MainWindow
from src.adjustment_start_game import Adjustment_Start_Game
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
    
    def open_pdf(self):
        # Путь к PDF файлу
        pdf_path = "data/Rules.pdf"
        
        try:
            # Открываем PDF с помощью системного приложения
            if sys.platform == "win32":
                subprocess.run(["start", pdf_path], shell=True)
            elif sys.platform == "darwin":  # Для macOS
                subprocess.run(["open", pdf_path])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть файл: {e}")
    
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
        self.game = Game()
        self.game.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())

