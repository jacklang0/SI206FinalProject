import matplotlib.pyplot as plt
import os
import sqlite3
import numpy as np

#1. Pie chart: Wealth of US vs Top 100 billionaries

#2. Bar graph: Count of Forbes 400 by Country, Split by Gender
def graph_count_by_country(cur, conn):

    sql = """
    SELECT c.country,
        count(f.id) as total,
        SUM(CASE WHEN f.gender = 'M' THEN 1 ELSE 0 END) AS mcount,
        SUM(CASE WHEN f.gender = 'F' THEN 1 ELSE 0 END) AS fcount,
        SUM(CASE WHEN f.gender IS NULL THEN 1 ELSE 0 END) AS nacount
    FROM CountryWealth c
    INNER JOIN ForbesPeople f on f.country_id = c.key
    GROUP BY c.country
    ORDER BY 2 DESC
    """

    results = cur.execute(sql).fetchall()
    country_label = [x[0] for x in results]
    mcount = np.array([x[2] for x in results])
    fcount = np.array([x[3] for x in results])
    nacount = np.array([x[4] for x in results])

    bar_width = 0.8

    fig, ax = plt.subplots(figsize=(16,10))
    

    ax.barh(country_label, mcount, bar_width, label = 'Male')
    ax.barh(country_label, fcount, bar_width, left = mcount, label = 'Female')
    ax.barh(country_label, nacount, bar_width, left = mcount+fcount, label = 'NA')

    ax.set_xlabel('Number of Citizens in Forbes 400')
    ax.set_ylabel('Country')
    ax.set_title('Count of Forbes 400 by Country and Gender')
    ax.legend()
    ax.invert_yaxis()

    plt.savefig('CountryCounts.png')
    #plt.show()


#3. Pie chart: Count of Forbes 400 by Industry 

#4. Scatter plot: Number of Forbes 400 vs Gini Coef of Country

#5. Scatter plot: Age vs Net Worth Amoung Forbes 400
def graph_age_vs_net_worth(cur, conn):
    sql = """
    SELECT net_worth, age
    FROM ForbesPeople f
    """
    results = cur.execute(sql).fetchall()
    net_worth = np.array([x[0] for x in results])
    age = np.array([x[1] for x in results])

    fig, ax = plt.subplots(figsize=(16,10))

    ax.scatter(age, net_worth)

    ax.set_xlabel('Age')
    ax.set_ylabel('Net Worth (Millions)')
    ax.set_title('Age vs Net Worth in Forbes 400')

    plt.savefig('AgeVsNetworth.png')
    #plt.show()


# Don't change anything in this function
def set_up_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    cur, conn = set_up_database('Wealth.db')

    graph_count_by_country(cur, conn)
    graph_age_vs_net_worth(cur, conn)

main()
