from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QRectF
import sys


class PlayingChip(QWidget):
    def __init__(self, parent=None, num=0, size=200):
        super().__init__(parent)

        self.size = size
        self.setFixedSize(size, size)
        self.num = num
    
    def add_chips(self, n):
        self.num += n
        self.update()
    
    def reset_to_zero(self):
        result = self.num
        self.num = 0
        self.update()
        return result

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        outer_radius = self.size // 2
        inner_radius = outer_radius * 0.6
        center = self.size // 2

        # Наружный серый круг
        painter.setBrush(QBrush(QColor(200, 200, 200)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(center - outer_radius, center - outer_radius, 
                                   2 * outer_radius, 2 * outer_radius))

        # Основные цветные секции
        num_sections = 8
        initial_offset = -22.5
        for i in range(num_sections):
            angle_start = initial_offset + (360 / num_sections) * i
            angle_span = 360 / num_sections

            color = QColor(255, 99, 71) if i % 2 == 0 else QColor(250, 250, 250)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPie(QRectF(center - outer_radius, center - outer_radius,
                                   2 * outer_radius, 2 * outer_radius), 
                            int(angle_start * 16), int(angle_span * 16))

        # Внутренний черный круг
        painter.setBrush(QBrush(QColor(128, 128, 128)))
        painter.drawEllipse(QRectF(center - inner_radius, center - inner_radius, 
                                   2 * (inner_radius), 2 * (inner_radius)))

        # Центральная белая область
        inner_white_radius = inner_radius * 0.8
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(QRectF(center - inner_white_radius, center - inner_white_radius,
                                   2 * inner_white_radius, 2 * inner_white_radius))


        painter.setPen(QColor(0, 0, 0))

        center_font_size = int(self.size / 3)
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        if self.num != '':
            top_rect = QRectF(0, 0, self.size, self.size)
            painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayingChip()
    ex.show()
    sys.exit(app.exec())
