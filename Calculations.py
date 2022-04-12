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

"""
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
"""

def get_countries_with_most_forbes400(cur, conn):
    cur.execute("""
        SELECT c.country,
            COUNT(f.id) as count
        FROM ForbesPeople f
        INNER JOIN CountryWealth c on c.key = f.country_id
        GROUP BY c.country
        ORDER BY 2 DESC
        """)
    results = cur.fetchall()[:5]
    return_str = "The 5 countries with the most citizens in the Forbes 400 are: "
    for result in results:
        return_str += (result[0] + " (" + str(result[1]) + ") ")

    return return_str

def get_industries_with_most_forbes400(cur, conn):
    cur.execute("""
        SELECT i.name,
            COUNT(f.id) as count
        FROM ForbesPeople f
        INNER JOIN Industries i on i.id = f.industry_id
        GROUP BY i.name
        ORDER BY 2 DESC
        """)
    results = cur.fetchall()[:3]
    return_str = "The 3 industries with the most citizens in the Forbes 400 are: "
    for result in results:
        return_str += (result[0] + " (" + str(result[1]) + ") ")

    return return_str

def get_wealth_of_top_N_US_forbes400(cur, conn, N):
    cur.execute("""
        SELECT net_worth
        FROM ForbesPeople F
        INNER JOIN CountryWealth c on c.key = f.country_id
        WHERE c.country = 'United States'
        """)
    results = cur.fetchall()[:N]

    return sum(i for i, in results)*1000000

def write_calcs_to_file(cur, conn):
    f = open("CalculatedData.txt", "w")
    
    f.write(get_countries_with_most_forbes400(cur, conn) + "\n")
    f.write(get_industries_with_most_forbes400(cur, conn) + "\n")
    x = round(total_wealth_US(161, cur, conn) / 1000000000000, 3)
    f.write("The total wealth of all adults in the United States is $" + str(x) + " trillion \n")
    x = round(get_wealth_of_top_N_US_forbes400(cur, conn, 100)/ 1000000000000, 3)
    f.write("The total wealth of the wealthiest 100 people in the US is $" + str(x) + " trillion \n")

    f.close()

def main():
    cur, conn = CountryWealthDistribution.setUpDatabase('Wealth.db')
    write_calcs_to_file(cur, conn)
    """
    US_total_wealth = total_wealth_US(161, cur, conn)
    print(f'Total US Wealth ${US_total_wealth}')

    gini_coefficients = get_gini(cur, conn)
    print("List of country's inequality percentage:")
    print(gini_coefficients)
    """

main()