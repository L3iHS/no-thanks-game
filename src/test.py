from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QFontMetrics

# Создаем экземпляр QApplication (для работы с графикой и шрифтами)
app = QApplication([])

# Устанавливаем шрифт
font = QFont("Arial", 12)

# Получаем метрики шрифта
font_metrics = QFontMetrics(font)

# Длина текста в пикселях
text = "Текущий игрок"
text_width = font_metrics.horizontalAdvance(text)

print(text_width)

# Завершаем приложение
app.quit()
