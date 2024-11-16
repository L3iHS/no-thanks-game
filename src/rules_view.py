import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class RuleWindow(QWidget):
    def __init__(self, image1_path, image2_path):
        super().__init__()
        self.setWindowTitle("Правила")
        self.resize(800, 400)
        
        # Основной layout
        self.layout = QVBoxLayout()
        
        # Горизонтальный layout для двух изображений
        self.image_layout = QHBoxLayout()
        
        # Метки для изображений
        self.image_label1 = QLabel("Изображение 1")
        self.image_label2 = QLabel("Изображение 2")
        
        self.image_label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.image_label1.setStyleSheet("border: 1px solid black;")
        self.image_label2.setStyleSheet("border: 1px solid black;")
        
        # Загружаем изображения в метки
        pixmap1 = QPixmap(image1_path)
        pixmap2 = QPixmap(image2_path)
        
        self.image_label1.setPixmap(pixmap1.scaled(self.image_label1.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.image_label2.setPixmap(pixmap2.scaled(self.image_label2.size(), Qt.AspectRatioMode.KeepAspectRatio))
        
        self.image_label1.setText("")  # Убираем текст
        self.image_label2.setText("")  # Убираем текст
        
        # Добавляем метки в горизонтальный layout
        self.image_layout.addWidget(self.image_label1)
        self.image_layout.addWidget(self.image_label2)
        
        # Добавляем все элементы в основной layout
        self.layout.addLayout(self.image_layout)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RuleWindow('/Users/iladroskov/Coding/Python/Yandex_Lyceum/no-thanks-game/data/data-1.png', '/Users/iladroskov/Coding/Python/Yandex_Lyceum/no-thanks-game/data/data-2.png')
    ex.show()
    sys.exit(app.exec())