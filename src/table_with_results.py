from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout,\
QHBoxLayout, QPushButton, QFrame, QLineEdit, QSizePolicy, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt6.QtCore import Qt
import sys
import sqlite3
from datetime import datetime
# from src.playing_chip import PlayingChip
# from src.playing_card import PlayingCard
# from src.playing_deck import PlayingDeck
# from src.random_chips import RandomChips


class TableWithResults(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(610, 400)
        self.setWindowTitle("Результаты игроков")

        self.table_results = QTableWidget(self)
        self.table_results.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_results.setColumnWidth(3, 150)
        self.table_results.resize(600, 400)
        self.table_results.setColumnCount(4)
        self.table_results.setHorizontalHeaderLabels(["Место", "Имя", "Результат", "Дата"])
    
    def add_player(self, name, score):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Определяем место для нового игрока (по возрастанию результатов)
        cur.execute('SELECT place, name, score FROM results ORDER BY score DESC, date ASC')
        results = cur.fetchall()

        place = 1
        for result in results:
            if score < result[2]:  # Если новый игрок набрал меньше баллов
                break
            place += 1  # Иначе, увеличиваем место

        # Обновляем места всех игроков, чьи места будут увеличены
        cur.execute('''
            UPDATE results
            SET place = place + 1
            WHERE place >= ?
        ''', (place,))

        # Добавляем нового игрока на его место
        cur.execute('''
            INSERT INTO results (place, name, score, date)
            VALUES (?, ?, ?, ?)
        ''', (place, name, score, date))

        # Сохраняем изменения
        con.commit()
        con.close()
        return place, date
    
    def output_results(self):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()

        cur.execute('''
            SELECT place, name, score, date
            FROM results
            ORDER BY place ASC
        ''')
        rows = cur.fetchall()

        # Устанавливаем количество строк в таблице
        self.table_results.setRowCount(len(rows))

        # Находим максимальное количество цифр в месте
        # max_place = max([len(row[0]) for row in rows])
        # place_width = len(str(max_place))
        # print(place_width)
        place_width = len(str(len(rows)))

        rows.sort(key=lambda x: int(x[0]))

        # Заполняем таблицу данными
        for row, row_data in enumerate(rows):
            for col, value in enumerate(row_data):
                if col == 0:  # Форматируем place
                    value = int(value)
                    value = "{:0{width}d}".format(value, width=place_width)
                self.table_results.setItem(row, col, QTableWidgetItem(str(value)))

        # Закрываем соединение
        con.close()

        self.update()
        # Показываем окно
        self.show()
    
    def print_result(self, date, name):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()

        result = cur.execute('''
            SELECT place, name, score
            FROM results
            WHERE date = ? AND name = ?
            ORDER BY score DESC
        ''', (date, name)).fetchall()

        con.close()
        return result[0]
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableWithResults()
    window.show()
    sys.exit(app.exec())
