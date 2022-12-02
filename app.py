import sqlite3
from flask import Flask, render_template, redirect, request, json, jsonify, g, url_for
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('./db/DataAnalyzer.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/db')
def db():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    rows = connection.execute("SELECT * FROM Referentiel")

    return render_template('index.html', rows=rows.fetchall())

@app.route('/db/json', methods=["GET"])
def jsonData():
    connection = get_db_connection()
    rows = connection.execute("SELECT * FROM Referentiel").fetchall()
    return jsonify(rows)

# debug
if __name__ == "__main__":
    app.run(debug=True)