import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt
import datetime
from datetime import date

# Reads json from cache
def read_cache(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cache_cont = f.read()
        data = json.loads(cache_cont)
        return data
    except:
        return {}

# Saves json in a local cache 
def write_cache(data, filename):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file_path = dir_path + '/' + filename
    
    data_json = json.dumps(data)
    with open(cache_file_path, 'w') as f:
        f.write(data_json)

# Calls Forbes400 API to get json of Forbes list
def call_api():
    request_url = "https://forbes400.herokuapp.com/api/forbes400"
    resp = requests.get(request_url)
    data = json.loads(resp.content)
    return data

# Sets up connection to the Wealth.db 
def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

# Creates ForbesPeople and Industries tables in db
def create_tables(cur, conn):
    sql = """
        CREATE TABLE IF NOT EXISTS ForbesPeople (
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE, 
            gender TEXT,
            country_id INTEGER,
            industry_id INTEGER,
            net_worth FLOAT,
            age INTEGER
        )
    """
    cur.execute(sql)

    sql = """
        CREATE TABLE IF NOT EXISTS Industries (
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE
        )
    """
    cur.execute(sql)
    conn.commit()

def get_key_counter(cur, table_name):
    id_var = "id"
    if table_name == "CountryWealth":
        id_var = "key"
    
    sql = f"SELECT MAX({id_var}) FROM {table_name}"

    try:
        cur.execute(sql)
        results = cur.fetchall()
        return results[-1][0] + 1
    except:
        return 0
    
"""
def insert_into_countries(cur, conn, data, n = 25):
    id = get_key_counter(cur, "Countries")
    id_limit = id + n

    for dict in data:
        id = get_key_counter(cur, "Countries")
        if id >= id_limit:
            break
        country = dict['countryOfCitizenship']
        cur.execute("INSERT OR IGNORE INTO Countries (id, name) VALUES (?,?)",(id, country))
        

    conn.commit()
"""

def insert_into_industries(cur, conn, data, n = 25):
    id = get_key_counter(cur, "Industries")
    id_limit = id + n

    for dict in data:
        id = get_key_counter(cur, "Industries")
        if id >= id_limit:
            break
        industry = dict['industries'][0]
        cur.execute("INSERT OR IGNORE INTO Industries (id, name) VALUES (?,?)",(id, industry))
        
    conn.commit()

def insert_into_people(cur, conn, data, n = 25):
    id = get_key_counter(cur, "ForbesPeople")
    id_limit = id + n

    for dict in data:
        id = get_key_counter(cur, "ForbesPeople")
        if id >= id_limit:
            break
        name = dict['personName']
        gender = dict.get('gender', None)

        country_name = dict['countryOfCitizenship']

        if country_name == "Czechia":
            country_name = "Czech Republic"
        elif country_name == "South Korea":
            country_name = "Korea"

        try:
            cur.execute("SELECT key from CountryWealth where country = ?", (country_name,))
            country_id = cur.fetchone()[0]
        except:
            # insert new country into CountryWealth
            country_id = get_key_counter(cur, "CountryWealth")
            cur.execute("INSERT OR IGNORE INTO CountryWealth (key, country, adults_in_thousands, mean_wealth_per_adult, median_wealth_per_adult, percent_under_10k, percent_10K_100k, percent_100K_1M, percent_over_1M, gini_percent) VALUES (?,?,?,?,?,?,?,?,?,?)",(country_id, country_name, None, None, None, None, None, None, None, None))
            conn.commit()

        industry_name = dict['industries'][0]
        cur.execute("SELECT id from Industries where name = ?", (industry_name,))
        industry_id = cur.fetchone()[0]

        net_worth = dict['finalWorth']

        try:
            today = date.today() 
            birth_date = int((dict['birthDate']) / 1000)
            birth_datetime = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(birth_date))
            age = today.year - birth_datetime.year - ((today.month, today.day) < (birth_datetime.month, birth_datetime.day))
        except:
            age = None

        cur.execute("INSERT OR IGNORE INTO ForbesPeople (id, name, gender, country_id, industry_id, net_worth, age) VALUES (?,?,?,?,?,?,?)",(id, name, gender,  country_id, industry_id, net_worth, age))

    conn.commit()


def main():
    filename = "cache_forbes.json"
    data = call_api()
    write_cache(data, filename)

    cur, conn = set_up_database("Wealth.db")
    create_tables(cur, conn)

    data = read_cache(filename)

    insert_into_industries(cur, conn, data)
    #insert_into_people(cur, conn, data)


if __name__ == "__main__":
    main()
