import requests
import sqlite3
from fastapi import FastAPI
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

# retrieve or create sqlite3 db
connection = sqlite3.connect("DataAnalyzer.db")
# write csv data to a new table
freq_data = pd.read_csv('frequentation_gares_2015_2021.csv')
freq_data.to_sql('Frequentation', connection, if_exists='replace', index=False)

cursor = connection.cursor()

rows = cursor.execute("SELECT * FROM Frequentation").fetchall()

class Data(Resource):
    def get(self):
        data = cursor.execute("SELECT * FROM Frequentation").fetchall()
        return {'data': data}, 200  # return data and 200 OK code


api.add_resource(Data, '/db')

if __name__ == '__main__':
    app.run()  # run Flask app