# This code creates a web server using the Flask framework,
# and exposes a route '/db/search' that performs a search in the SQLite3 database 'DataAnalyzer.db'

import sqlite3
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template, redirect, request, json, jsonify, g, url_for
from flask_restful import Resource, Api, reqparse
import json
import unittest
import os
import collections
from datetime import date
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DB = os.getenv('DB')

@app.route('/db/search', methods=["GET"])
#This function performs a search in the SQLite3 database 'DataAnalyzer.db' based on the parameters passed in the request query string, such as 'region' and 'zipcode'
def search():
    # Connecting to the SQLite3 database 'DataAnalyzer.db'
    connection = sqlite3.connect(DB)
    cur = connection.cursor()
    args = request.args
    regionquery = args.get("region")
    cp = args.get("zipcode")
    
    if not regionquery:
        cur.execute("SELECT [fields.gare_alias_libelle_noncontraint], [fields.gare_regionsncf_libelle], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel WHERE [fields.adresse_cp] = "+cp)
        # Retrieving the data from the referentiel table where the zipcode matches query
    if not cp:
        region = regionquery.upper()
        cur.execute("SELECT [fields.gare_alias_libelle_noncontraint], [fields.gare_regionsncf_libelle], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel WHERE [fields.gare_regionsncf_libelle] = '"+region+"'")
        # Retrieving the data from the referentiel table where the region matches query

    i = 0

    while True:
        i += 1
        rows = cur.fetchall()

        rowarray_list = []

        for row in rows:
            t = (row[0], row[1], row[2], row[3], row[4])
            rowarray_list.append(t)
        j = json.dumps(rowarray_list)

        # Convert query to objects of key-value pairs
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d["nom_gare"] = row[0]
            d["region"] = row[1]
            d["zipcode"] = row[2]
            d["departement"] = row[3]
            d["uic_code"] = row[4]
            objects_list.append(d)
            
        j = json.dumps(objects_list)
        i = 0

        return json.dumps(objects_list), 200
        # Returning the data in JSON format
        
### swagger specific ###
SWAGGER_URL = '/db/docs'
API_URL = "/db/swgdef"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Data Analyzer"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/db/swgdef')
def swgdef(): return open('./swagger.json')
### end swagger specific ###

@app.route('/db/test')
class TestApp(unittest.TestCase):
    def test_search(self):
        response = self.app.get('/db/search?region=region&zipcode=zipcode')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'nom_gare', response.data)
        self.assertIn(b'reg')
                      
# debugs
if __name__ == "__main__":
    app.run(port = PORT)
