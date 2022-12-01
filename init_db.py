import sqlite3
import pandas as pd

# create sqlite3 db
connection = sqlite3.connect("DataAnalyzer.db", check_same_thread=False)
# write csv data to a new table
freq_data = pd.read_csv('frequentation-gares.csv')
freq_data.to_sql('Frequentation', connection, if_exists='replace', index=False)