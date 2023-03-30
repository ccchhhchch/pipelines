import sqlite3
import pandas as pd
import re
import csv
name = 'database.db'
def load(file, table):
    database = sqlite3.connect(name)
    pd.read_csv(f'{file}').to_sql(name=table, con=database, if_exists='append', index=False)
def get_domain(url):
    temp = "((?<=http:\/\/)|(?<=https:\/\/)).+?(?=\/)"
    result = re.search(temp, str(url)).group(0)
    return result
def create(table, query):
    database = sqlite3.connect(name)
    database.create_function("domain_of_url", 1, get_domain)
    database.execute("create table if not exists " + table + " as " + query)
def save(file, table):
    database = sqlite3.connect(name)
    dataframe = pd.read_sql_query("SELECT * FROM " + table, database)
    dataframe.to_csv(file + ".csv", index=False)
def sql(query):
    database = sqlite3.connect(name)
    database.execute(query)
    database.commit()
