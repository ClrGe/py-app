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
### end swagger specific ###



@app.route('/db/swgdef')
def swgdef(): return open('./swagger.json')


@app.route('/db/search', methods=["GET"])
def search():

    connection = sqlite3.connect('data/DataAnalyzer.db')
    cur = connection.cursor()

    args = request.args
    regionquery = args.get("region")
    cp = args.get("zipcode")
    
    if not regionquery:
        cur.execute("SELECT [fields.gare_alias_libelle_noncontraint], [fields.gare_regionsncf_libelle], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel WHERE [fields.adresse_cp] = "+cp)
    if not cp:
        region = regionquery.upper()
        cur.execute("SELECT [fields.gare_alias_libelle_noncontraint], [fields.gare_regionsncf_libelle], [fields.adresse_cp],  [fields.departement_libellemin], [fields.uic_code] FROM referentiel WHERE [fields.gare_regionsncf_libelle] = '"+region+"'")

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
