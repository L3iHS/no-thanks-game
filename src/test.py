import sqlite3

# Создаем или подключаемся к существующей базе данных
# con = sqlite3.connect("data/results.sqlite")
# cur = con.cursor()

# # Создаем таблицу с колонками: место, имя, результат, дата
# cur.execute('''
# CREATE TABLE IF NOT EXISTS results (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     place TEXT,
#     name TEXT,
#     score INTEGER,
#     date TEXT
# )
# ''')

# # Сохраняем изменения и закрываем соединение
# con.commit()
# con.close()

# print("База данных успешно создана!")



#################Очистка базы данных
con = sqlite3.connect("data/results.sqlite")
cur = con.cursor()

# Удаляем все записи из таблицы
cur.execute('DELETE FROM results')

# Сохраняем изменения
con.commit()
con.close()
