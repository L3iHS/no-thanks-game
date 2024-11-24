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

        # Определяем место для нового игрока
        results = cur.execute('SELECT id, place, name, score FROM results ORDER BY score DESC, date ASC').fetchall()

        place = cur.execute("""SELECT MAX(place) FROM results
                            WHERE score <= ?""", (score,)).fetchall()
        if not place or not place[0][0]:
            place = 1 
        else:
            place = place[0][0] + 1  

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

        self.table_results.setRowCount(len(rows))
        for row, row_data in enumerate(rows):
            for col, value in enumerate(row_data):
                self.table_results.setItem(row, col, QTableWidgetItem(str(value)))

        self.table_results.resizeColumnsToContents()
        self.table_results.resizeRowsToContents()

        con.close()
        self.update()
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