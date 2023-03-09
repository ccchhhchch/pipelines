import sqlite3
import pandas
import re
import csv
name = 'database.db'
def load(file, table):
    database = sqlite3.connect(name)
    pandas.read_csv(f'{file}').to_sql(name=table, con=database, if_exists='append', index=False)
def get_domain(url):
    temp = "((?<=http:\/\/)|(?<=https:\/\/)).+?(?=\/)"
    result = re.search(temp, str(url)).group(0)
    return result
def create(table, query):
    database = sqlite3.connect(name)
    database.create_function("domain_of_url", 1, get_domain)
    database.execute("create table if not exists " + table + " as " + query)
def save(file, table):
    with open(f"{file}.csv", "w") as file:
        cur = sqlite3.connect(name).cursor()
        writer = csv.writer(file)
        writer.writerow(['id', 'name', 'url', 'domain_of_url'])
        data = cur.execute("SELECT * FROM " + table)
        writer.writerows(data)
def sql(query):
    database = sqlite3.connect(name)
    database.execute(query)
    database.commit()
