from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF
import sys


class PlayingChip(QWidget):
    def __init__(self, parent=None, num=0, size=200):
        super().__init__(parent)
        self.size = size  # Размер фишки
        self.setFixedSize(size, size)
        self.num = num
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Основные параметры
        outer_radius = self.size // 2
        inner_radius = outer_radius * 0.6
        center = self.size // 2

        # 1. Наружный серый круг (контур фишки) с увеличенной толщиной
        painter.setBrush(QBrush(QColor(200, 200, 200)))  # Светло-серый цвет
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(center - outer_radius, center - outer_radius, 
                                   2 * outer_radius, 2 * outer_radius))

        # 2. Основные цветные секции (синие и белые)
        num_sections = 8
        initial_offset = -22.5  # Поворот, чтобы секции выровнялись по вертикали
        for i in range(num_sections):
            angle_start = initial_offset + (360 / num_sections) * i
            angle_span = 360 / num_sections

            # Чередуем цвета
            color = QColor(255, 99, 71) if i % 2 == 0 else QColor(250, 250, 250)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(QRectF(center - outer_radius, center - outer_radius,
                                   2 * outer_radius, 2 * outer_radius), 
                            int(angle_start * 16), int(angle_span * 16))

        # 3. Внутренний черный круг (второй контур)
        # painter.setPen(QPen(QColor(105, 105, 105)))
        painter.setBrush(QBrush(QColor(128, 128, 128)))  # Серый цвет
        painter.drawEllipse(QRectF(center - inner_radius, center - inner_radius, 
                                   2 * (inner_radius), 2 * (inner_radius)))

        # 4. Центральная белая область (пустое пространство)
        inner_white_radius = inner_radius * 0.8
        painter.setBrush(QBrush(QColor(255, 255, 255)))  # Белый цвет
        painter.drawEllipse(QRectF(center - inner_white_radius, center - inner_white_radius,
                                   2 * inner_white_radius, 2 * inner_white_radius))


        painter.setPen(QColor(0, 0, 0))  # Черный цвет для цифры

        # Установка шрифта для цифры
        center_font_size = int(self.size / 3)  # Пропорциональный размер шрифта для центральной цифры
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        # Цифра в верхней половине карты
        top_rect = QRectF(0, 0, self.size, self.size)
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayingChip()  # Устанавливаем размер фишки
    ex.show()
    sys.exit(app.exec())
