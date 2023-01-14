import sqlite3
from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, render_template, redirect, request, json, jsonify, g, url_for
from flask_restful import Resource, Api, reqparse
import json
import logging
import collections
from datetime import date

today = date.today()
d1 = today.strftime("%d%m%Y")
logging.basicConfig(filename='./data/logs_'+d1+'.log', level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/db/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Data Analyzer"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


def get_db_connection():
    connection = sqlite3.connect('data/DataAnalyzer.db')
    connection.row_factory = sqlite3.Row

    return connection


@app.route('/db')
def db():
    connection = get_db_connection()
    connection.row_factory = sqlite3.Row
    rows = connection.execute("SELECT code_uic FROM referentiel")

    return render_template('index.html', rows=rows.fetchall())


@app.route('/db/all', methods=["GET"])
def getData():

    connection = sqlite3.connect('data/DataAnalyzer.db')
    cur = connection.cursor()

    cur.execute(
        "SELECT [fields.gare_alias_libelle_noncontraint], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel")

    i = 0

    while True:
        i += 1
        rslt = cur.fetchall()
        jsonResult = json.dumps(rslt, indent=4, sort_keys=True)

        return json.dumps(cur.fetchall()), 200


@app.route('/db/search', methods=["GET"])
def search():

    connection = sqlite3.connect('data/DataAnalyzer.db')
    cur = connection.cursor()

    args = request.args
    cp = args.get("zipcode")
    cur.execute("SELECT [fields.gare_alias_libelle_noncontraint], [fields.gare_regionsncf_libelle], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel WHERE [fields.adresse_cp] = "+cp)

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
        #rslt = cur.fetchall()
        #jsonResult = json.dumps(rslt, indent=10, sort_keys=True)

        return json.dumps(objects_list), 200


# debugs
if __name__ == "__main__":
    app.run(debug = True)
