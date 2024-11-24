import sys
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtWidgets import QApplication, QWidget


class PlayingDeck(QWidget):
    def __init__(self, parent=None, num=1, size=(200, 300)):
        super().__init__(parent)

        self.num = num
        self.size = size
        self.setFixedSize(*size)
    
    def update_num(self, n):
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

        circle_radius = min(self.size) * 0.4
        circle_rect = QRectF(
            (self.size[0] - circle_radius * 2) / 2,
            (self.size[1] - circle_radius * 2) / 2,
            circle_radius * 2,
            circle_radius * 2
        )
        painter.setBrush(QColor(138, 102, 66))
        painter.setPen(Qt.GlobalColor.transparent)
        painter.drawEllipse(circle_rect)

        painter.setPen(QColor(0, 0, 0))

        center_font_size = int(self.size[0] / 2)
        center_font = QFont("American Typewriter", center_font_size)
        painter.setFont(center_font)

        top_rect = QRectF(0, 0, self.size[0], self.size[1])
        painter.drawText(top_rect, Qt.AlignmentFlag.AlignCenter, f"{self.num}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PlayingDeck(size=(600, 900), num=47)
    ex.show()
    sys.exit(app.exec())
