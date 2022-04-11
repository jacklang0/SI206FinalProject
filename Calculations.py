from bs4 import BeautifulSoup
import requests
import json
import re
import os
import sqlite3
import csv
import CountryWealthDistribution
import requests

def total_wealth_US(US_key, cur, con):
    cur.execute('SELECT adults_in_thousands, mean_wealth_per_adult FROM CountryWealth WHERE key = ?', (US_key,))
    results = cur.fetchall()[0]

    adults = results[0] * 1000
    mean_wealth = results[1]
    return adults*mean_wealth

def main():
    cur, conn = CountryWealthDistribution.setUpDatabase('Wealth.db')
    US_total_wealth = total_wealth_US(161, cur, conn)
    print(f'Total US Wealth ${US_total_wealth}')

main()