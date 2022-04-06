import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

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
            net_worth INTEGER,
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
    sql = f"SELECT MAX(key) FROM {table_name}"

    try:
        cur.execute(sql)
        results = cur.fetchall()
        return results[-1][0]
    except:
        return 0
    



def main():
    filename = "cache_forbes.json"
    #data = call_api()
    #write_cache(data, filename)

    cur, conn = set_up_database("Forbes400.db")
    create_tables(cur, conn)

    data = read_cache(filename)

    insert_n_rows_from_dict(cur, conn, data)

    return

if __name__ == "__main__":
    main()
