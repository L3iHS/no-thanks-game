from PyQt6.QtWidgets import QApplication, QMainWindow,QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt
import sys
import sqlite3
from datetime import datetime


class TableWithResults(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(380, 400)
        self.setWindowTitle("Результаты игроков")

        self.players = {}

        self.table_results = QTableWidget(self)
        self.table_results.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.table_results.resizeColumnsToContents()
        # self.table_results.resizeRowsToContents()

        self.table_results.horizontalHeader().ResizeMode(QHeaderView)
        self.table_results.show()
        self.table_results.setColumnWidth(3, 200)
        self.table_results.resize(370, 400)
        self.table_results.setColumnCount(4)
        self.table_results.setHorizontalHeaderLabels(["Место", "Имя", "Результат", "Дата"])
    
    def add_player(self, name, score):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Определяем место для нового игрока (по возрастанию результатов)
        results = cur.execute('SELECT id, place, name, score FROM results ORDER BY score DESC, date ASC').fetchall()

        place = cur.execute("""SELECT MAX(place) FROM results
                            WHERE score <= ?""", (score,)).fetchall()
        print(place)
        if not place or not place[0][0]:
            place = 1 
        else:
            place = place[0][0] + 1  

        # Добавляем нового игрока на его место
        cur.execute('''
            INSERT INTO results (place, name, score, date)
            VALUES (?, ?, ?, ?)
        ''', (place, name, score, date))

        # Обновляем места всех игроков, чьи места будут увеличены
        cur.execute('''
            UPDATE results
            SET place = place + 1
            WHERE score > ?
        ''', (score,))

        # Сохраняем изменения
        con.commit()
        con.close()
        return place, date
    
    def output_results(self):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()

        rows = cur.execute('''
            SELECT place, name, score, date
            FROM results
            ORDER BY score ASC
        ''').fetchall()

        # Устанавливаем количество строк в таблице
        self.table_results.setRowCount(len(rows))

        # place_width = len(str(len(rows)))

        # rows.sort(key=lambda x: int(x[0]))

        # Заполняем таблицу данными
        for row, row_data in enumerate(rows):
            for col, value in enumerate(row_data):
                # if col == 0:  # Форматируем place
                #     value = int(value)
                #     value = "{:0{width}d}".format(value, width=place_width)
                self.table_results.setItem(row, col, QTableWidgetItem(str(value)))

        self.table_results.resizeColumnsToContents()
        self.table_results.resizeRowsToContents()

        # Закрываем соединение
        con.close()

        self.update()
        # Показываем окно
        self.show()
    
    def print_result(self, date, name):
        con = sqlite3.connect("data/results.sqlite")
        cur = con.cursor()
        print(date, name)

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
