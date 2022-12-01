import requests
import sqlite3

connection = sqlite3.connect("DataAnalyzer.db")

cursor = connection.cursor()

rows = cursor.execute("SELECT * FROM Frequentation").fetchall()
print(rows)
