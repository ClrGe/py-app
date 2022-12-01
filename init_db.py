import sqlite3
import pandas as pd

# create sqlite3 db
connection = sqlite3.connect("DataAnalyzer.db", check_same_thread=False)
# write csv data to a new table
freq_data = pd.read_csv('referentiel-gares.csv')
freq_data.to_sql('Referentiel', connection, if_exists='replace', index=False)

connection.commit()