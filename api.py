import requests
import sqlite3
from fastapi import FastAPI
from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

# retrieve and use local sqlite db
connection = sqlite3.connect("DataAnalyzer.db")
cursor = connection.cursor()
rows = cursor.execute("SELECT * FROM Frequentation").fetchall()

class Users(Resource):
    def get(self):
        data = pd.read_csv('../data/frequentation_gares_2015_2021.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data': data}, 200  # return data and 200 OK code
    
class Locations(Resource):
    rows = cursor.execute("SELECT * FROM Frequentation").fetchall()
    pass
    
api.add_resource(Users, '/db')  # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations

if __name__ == '__main__':
    app.run()  # run our Flask app