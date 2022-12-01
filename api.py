import requests
import sqlite3
from fastapi import FastAPI
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import render_template, redirect, request    
import ast

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('DataAnalyzer.db', check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/db')
def index():
    connection = get_db_connection()
    gares = connection.execute("SELECT * FROM Frequentation").fetchall()
    connection.close()
    return render_template('index.html', gares=gares)

# debug
if __name__ == "__main__":
    app.run(debug=True)