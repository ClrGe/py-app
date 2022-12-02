import sqlite3
from flask import Flask, render_template, redirect, request, json, jsonify, g, url_for
from flask_restful import Resource, Api, reqparse
import json
import logging
from datetime import date

today = date.today()
d1 = today.strftime("%d%m%Y")
logging.basicConfig(filename='./data/logs_'+d1+'.log', level=logging.INFO, format=f'%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)

#api = Api(app=app, version="1.0", doc="/db/api", title="Data analyzer DB service", description="Sqlite3 / Python-Flask", default="API", default_label='', validate=True)

def get_db_connection():
    connection = sqlite3.connect('data/DataAnalyzer.db')
    connection.row_factory = sqlite3.Row

    return connection

@app.route('/db')
def db():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    rows = connection.execute("SELECT * FROM Referentiel")

    return render_template('index.html', rows=rows.fetchall())


@app.route('/db/json', methods=["GET"])
def getData():

    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Referentiel LIMIT 1")
    result = cursor.fetchall()
    jsonResult = json.dumps(result, indent=4, sort_keys=True, default=str)

    return json.loads(jsonResult), 200

# debugs
if __name__ == "__main__":
    app.run(debug=True)