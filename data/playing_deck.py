import sys
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget


class PlayingDeck(QWidget):
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

        circle_radius = min(self.size) * 0.4  # Радиус круга — 25% от меньшей стороны карты
        circle_rect = QRectF(
            (self.size[0] - circle_radius * 2) / 2,  # Центр по X
            (self.size[1] - circle_radius * 2) / 2,  # Центр по Y
            circle_radius * 2,  # Ширина круга
            circle_radius * 2   # Высота круга
        )
        painter.setBrush(QColor(138, 102, 66))  # Цвет круга
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawEllipse(circle_rect)

        painter.setPen(QColor(0, 0, 0))  # Черный цвет для цифры

        # Установка шрифта для цифры
        center_font_size = int(self.size[0] / 2)  # Пропорциональный размер шрифта для центральной цифры
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        # Цифра в верхней половине карты
        top_rect = QRectF(0, 0, self.size[0], self.size[1])
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PlayingDeck(size=(600, 900), num=47)
    ex.show()  # Окно будет отображать размер карты
    sys.exit(app.exec())
