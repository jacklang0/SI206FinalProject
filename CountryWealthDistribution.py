from bs4 import BeautifulSoup
import requests
import json
import re
import os
import sqlite3
import csv
import unittest
import requests


def get_website_info():
    url = "https://en.wikipedia.org/wiki/Distribution_of_wealth"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    div = soup.find("div", id="content")
    body_content = div.find("div", id="bodyContent")
    content_text = body_content.find("div", id="mw-content-text")
    parser_output = content_text.find("div", class_="mw-parser-output")
    table = parser_output.find("table", class_="wikitable")
    tbody = table.find("tbody")
    tr = tbody.find_all("tr")
    tds = []

    lst_all_countries = []
    
    for row in tr:
        tds = row.find_all("td")
        if len(tds) > 0:
            country_lst = []
            for index in range(len(tds)):
                if index == 0:
                    country_lst.append(tds[index].text.strip())
                elif index==1 or index==2 or index==3:
                    country_lst.append(int(tds[index].text.strip().replace(",","")))
                else:
                    country_lst.append(float(tds[index].text.strip()))
            lst_all_countries.append(country_lst)
    return lst_all_countries

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def get_key_counter(cur):
    try:
        cur.execute('SELECT MAX(key) FROM CountryWealth')
        results = cur.fetchall()
        return results[-1][0]
    except:
        return 0


def create_website_database(wealth_info, cur, conn, counter):
    countries = []
    adults_thousands = []
    mean_wealth = []
    median_wealth = []
    under_10k = []
    _10k_100k = []
    _100k_1m = []
    over_1m = []
    gini = []

    for item_list in wealth_info:
        countries.append(item_list[0])
        adults_thousands.append(item_list[1])
        mean_wealth.append(item_list[2])
        median_wealth.append(item_list[3])
        under_10k.append(item_list[4])
        _10k_100k.append(item_list[5])
        _100k_1m.append(item_list[6])
        over_1m.append(item_list[7])
        gini.append(item_list[8])

    cur.execute("CREATE TABLE IF NOT EXISTS CountryWealth (key INTEGER PRIMARY KEY, country TEXT, adults_in_thousands INTEGER, mean_wealth_per_adult INTEGER, median_wealth_per_adult INTEGER, percent_under_10k FLOAT, percent_10K_100k FLOAT, percent_100K_1M FLOAT, percent_over_1M FLOAT, gini_percent FLOAT)")
    key_counter_to_limit = 0
    key_counter = counter
    for index in range(counter, len(countries), 1):
        if key_counter_to_limit >= 25:
             break
        else:
            cur.execute("INSERT OR IGNORE INTO CountryWealth (key, country, adults_in_thousands, mean_wealth_per_adult, median_wealth_per_adult, percent_under_10k, percent_10K_100k, percent_100K_1M, percent_over_1M, gini_percent) VALUES (?,?,?,?,?,?,?,?,?,?)",(key_counter, countries[index], adults_thousands[index], mean_wealth[index], median_wealth[index], under_10k[index], _10k_100k[index], _100k_1m[index], over_1m[index], gini[index]))
            key_counter_to_limit+=1
            key_counter+=1
    conn.commit()
    
def main():
   

    wealth_info = get_website_info()
    cur, conn = setUpDatabase('Wealth.db')
    counter = get_key_counter(cur)
    print(counter)
    create_website_database(wealth_info, cur, conn, counter)
main()
