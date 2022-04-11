from bs4 import BeautifulSoup
import requests
import json
import re
import os
import sqlite3
import csv
import CountryWealthDistribution
import requests

def total_wealth_US(US_key, cur, conn):
    cur.execute('SELECT adults_in_thousands, mean_wealth_per_adult FROM CountryWealth WHERE key = ?', (US_key,))
    results = cur.fetchall()[0]

    adults = results[0] * 1000
    mean_wealth = results[1]
    return adults*mean_wealth
#Get top 5 billionaries
#Wealth of US vs Top 5 billionaries - pie chart


#Calculate a list of gini-coefficients
def get_gini(cur, conn):
    cur.execute('SELECT gini_percent FROM CountryWealth')
    results = cur.fetchall()
    gini_list = []

    for item in results:
        gini_list.append(item[-1])

    return gini_list
#Get number of billionaries in each and make it a dictionary
#Plot scatterplot of number of billionaries vs gini-coefficient

#Industry pie chart

#Bar chart of countries on Forbes table, sum up each country's total wealth in the Forbes400

def main():
    cur, conn = CountryWealthDistribution.setUpDatabase('Wealth.db')
    US_total_wealth = total_wealth_US(161, cur, conn)
    print(f'Total US Wealth ${US_total_wealth}')

    gini_coefficients = get_gini(cur, conn)
    print("List of country's inequality percentage:")
    print(gini_coefficients)

main()