import sys
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtWidgets import QApplication, QWidget


class PlayingCard(QWidget):
    card_cleared = pyqtSignal()

    def __init__(self, parent=None, num=1, size=(200, 300)):
        super().__init__(parent)

        self.num = num
        self.size = size
        self.setFixedSize(*size)
        self.backlight = False

    def active_backlight(self):
        self.backlight = True
        self.update()
    
    def deactive_backlight(self):
        self.backlight = False
        self.update()

    def update_num(self, n):
        if self.num != '' and n == '':
            self.card_cleared.emit()  # Сигнал когда карта очищена

        self.num = n
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Основная часть карты
        corner_radius = min(self.size) * 0.075
        card_rect = QRectF(0, 0, *self.size)
        painter.setBrush(QColor(222, 184, 135))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(card_rect, corner_radius, corner_radius)

        # Обводка
        if self.backlight:
            corner_radius = min(self.size) * 0.075
            card_rect = QRectF(0, 0, self.size[0], self.size[1])
            painter.setBrush(Qt.GlobalColor.transparent)
            painter.setPen(QPen(QColor(255, 0, 0), self.size[0] / 24))
            painter.drawRoundedRect(card_rect, corner_radius, corner_radius)

        # Внутреннее очертание карты
        corner_radius = min(self.size) * 0.075
        card_rect = QRectF(self.size[0] * 0.18, self.size[1] * 0.10, self.size[0] * 0.64, self.size[1] * 0.80)
        painter.setBrush(QColor(138, 102, 66))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawRoundedRect(card_rect, corner_radius, corner_radius)

        painter.setPen(QColor(0, 0, 0))

        corner_font_size = int(self.size[0] / 6)
        font = QFont("American Typewriter", corner_font_size)
        painter.setFont(font)

        # Цифра в левом верхнем углу карты
        top_left_rect = QRectF(self.size[0] / 40, 0, self.size[0] / 4, self.size[1] / 8)  # Прямоугольник для выравнивания
        painter.drawText(top_left_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"{self.num}")

        painter.setPen(QColor(0, 0, 0))

        center_font_size = int(self.size[0] / 2)
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        # Цифра в верхней половине карты
        top_rect = QRectF(0, 0, self.size[0], self.size[1] / 2)
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

        # Цифра в нижней половине карты
        bottom_rect = QRectF(0, self.size[1] / 2, self.size[0], -self.size[1] / 2)
        painter.save()
        painter.translate(self.size[0], self.size[1])
        painter.rotate(180)
        painter.drawText(bottom_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

        corner_font_size = int(self.size[0] / 6)
        font = QFont("American Typewriter", corner_font_size)
        painter.setFont(font)
        bottom_right_rect = QRectF(self.size[0] * 1/40, 0, self.size[0], self.size[1])
        painter.drawText(bottom_right_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, f"{self.num}")

        painter.restore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PlayingCard(size=(600, 900), num=47)
    ex.show()
    sys.exit(app.exec())
