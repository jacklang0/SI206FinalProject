import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt
import datetime
from datetime import date

def read_cache(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            cache_cont = f.read()
        data = json.loads(cache_cont)
        return data
    except:
        return {}

def write_cache(data, filename):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache_file_path = dir_path + '/' + filename
    
    data_json = json.dumps(data)
    with open(cache_file_path, 'w') as f:
        f.write(data_json)

def call_api():
    request_url = "https://forbes400.herokuapp.com/api/forbes400"
    resp = requests.get(request_url)
    data = json.loads(resp.content)
    return data

def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_tables(cur, conn):
    sql = """
        CREATE TABLE IF NOT EXISTS People (
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
        CREATE TABLE IF NOT EXISTS Countries (
            id INTEGER PRIMARY KEY, 
            name TEXT UNIQUE
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
    sql = f"SELECT MAX(id) FROM {table_name}"

    try:
        cur.execute(sql)
        results = cur.fetchall()
        return results[-1][0] + 1
    except:
        return 0
    

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
    id = get_key_counter(cur, "People")
    id_limit = id + n

    for dict in data:
        id = get_key_counter(cur, "People")
        if id >= id_limit:
            break
        name = dict['personName']
        gender = dict.get('gender', None)

        country_name = dict['countryOfCitizenship']
        cur.execute("SELECT id from Countries where name = ?", (country_name,))
        country_id = cur.fetchone()[0]
        

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

        cur.execute("INSERT OR IGNORE INTO People (id, name, gender, country_id, industry_id, net_worth, age) VALUES (?,?,?,?,?,?,?)",(id, name, gender,  country_id, industry_id, net_worth, age))

    conn.commit()




    conn.commit()
def main():
    filename = "cache_forbes.json"
    #data = call_api()
    #write_cache(data, filename)

    cur, conn = set_up_database("Forbes400.db")
    create_tables(cur, conn)

    data = read_cache(filename)

    #insert_into_countries(cur, conn, data)
    #insert_into_industries(cur, conn, data)
    insert_into_people(cur, conn, data)


if __name__ == "__main__":
    main()
