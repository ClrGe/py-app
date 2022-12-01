import requests
import sqlite3
from fastapi import FastAPI

app = FastAPI()

# retrieve and use local sqlite db
connection = sqlite3.connect("DataAnalyzer.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT * FROM Frequentation").fetchall()


@app.get('/db')
def data():
    return {rows}
