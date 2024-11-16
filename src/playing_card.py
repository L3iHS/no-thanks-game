import sys
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget


class PlayingCard(QWidget):
    def __init__(self, parent=None, num=1, size=(200, 300)):
        super().__init__(parent)

        self.num = num
        self.size = size
        self.setFixedSize(*size)  # Устанавливаем размер карты

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Основная часть карты с закругленными углами и бежевым цветом
        corner_radius = min(self.size) * 0.075  # Закругление углов (10% от меньшей стороны карты)
        card_rect = QRectF(0, 0, *self.size)
        painter.setBrush(QColor(222, 184, 135))  # Бежевый цвет
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(card_rect, corner_radius, corner_radius)  # Закругленные углы

        # Внутреннее очертание карты
        corner_radius = min(self.size) * 0.075  # Закругление углов (10% от меньшей стороны карты)
        card_rect = QRectF(self.size[0] * 0.18, self.size[1] * 0.10, self.size[0] * 0.64, self.size[1] * 0.80)
        painter.setBrush(QColor(138, 102, 66))  # Бежевый темный цвет
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(card_rect, corner_radius, corner_radius)  # Закругленные углы

        painter.setPen(QColor(0, 0, 0))  # Черный цвет для цифры

        # Установка шрифта для цифры в углу
        corner_font_size = int(self.size[0] / 6)  # Пропорциональный размер шрифта для цифры в углу 
        font = QFont("American Typewriter", corner_font_size)
        painter.setFont(font)

        # Цифра в левом верхнем углу карты
        top_left_rect = QRectF(self.size[0] / 40, 0, self.size[0] / 4, self.size[1] / 8)  # Прямоугольник для выравнивания
        painter.drawText(top_left_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"{self.num}")

        # Установка цвета пера для цифры
        painter.setPen(QColor(0, 0, 0))  # Черный цвет для цифры

        # Установка шрифта для цифры
        center_font_size = int(self.size[0] / 2)  # Пропорциональный размер шрифта для центральной цифры
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        # Цифра в верхней половине карты
        top_rect = QRectF(0, 0, self.size[0], self.size[1] / 2)
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

        # Цифра в нижней половине карты (перевернутая)
        # Смещаем нижнюю половину на 180 градусов
        bottom_rect = QRectF(0, self.size[1] / 2, self.size[0], -self.size[1] / 2)
        painter.save()  # Сохраняем текущую трансформацию
        painter.translate(self.size[0], self.size[1])  # Перемещаем в нижний правый угол
        painter.rotate(180)  # Поворачиваем на 180 градусов
        painter.drawText(bottom_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

        # Установка шрифта для цифры в углу
        corner_font_size = int(self.size[0] / 6)  # Пропорциональный размер шрифта для цифры в углу 
        font = QFont("American Typewriter", corner_font_size)
        painter.setFont(font)
        # Цифра в левом верхнем углу карты
        bottom_right_rect = QRectF(self.size[0] * 1/40, 0, self.size[0], self.size[1])  # Прямоугольник для выравнивания
        painter.drawText(bottom_right_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"{self.num}")

        painter.restore()  # Восстанавливаем трансформацию

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PlayingCard(size=(600, 900), num=47)
    ex.show()  # Окно будет отображать размер карты
    sys.exit(app.exec())
