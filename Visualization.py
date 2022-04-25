import matplotlib.pyplot as plt
import os
import sqlite3
import numpy as np

#1. Pie chart: Wealth of US vs Top 100 billionaries
def graph_top_100_vs_total_US_wealth(cur, conn):

    #Finding total wealth
    US_key = 161
    cur.execute('SELECT adults_in_thousands, mean_wealth_per_adult FROM CountryWealth WHERE key = ?', (US_key,))
    results = cur.fetchall()[0]

    adults = results[0] * 1000
    mean_wealth = results[1]
    total_US_wealth = adults*mean_wealth

    #Getting Top 100 in US population
    cur.execute("""
        SELECT net_worth
        FROM ForbesPeople F
        INNER JOIN CountryWealth c on c.key = f.country_id
        WHERE c.country = 'United States'
        """)
    results = cur.fetchall()[:100]
    total_100_US = sum(i for i, in results)*1000000

    labels = 'Top 100 billonaries', 'Remaining 334 Million People'
    sizes = [total_100_US/total_US_wealth, (1 - total_100_US/total_US_wealth)]
    colors = ['red', 'lightblue']
    explode = (0.1, 0)
    fig, ax = plt.subplots(figsize=(16,10))
    ax.set_title('Top 100 US Billionaires vs. Rest of Population as a Percentage of Total US Wealth')
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct = '%1.1f%%')
    #plt.show()
    plt.savefig('Top100USBillionaires.png')

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


#3. Bar graph: Count of Forbes 400 by Industry 
def graph_count_of_forbes_by_industry(cur, conn):
    cur.execute("""
        SELECT i.name,
            COUNT(f.id) as count,
            SUM(CASE WHEN f.gender = 'M' THEN 1 ELSE 0 END) AS mcount,
            SUM(CASE WHEN f.gender = 'F' THEN 1 ELSE 0 END) AS fcount,
            SUM(CASE WHEN f.gender IS NULL THEN 1 ELSE 0 END) AS nacount
        FROM ForbesPeople f
        INNER JOIN Industries i on i.id = f.industry_id
        GROUP BY i.name
        ORDER BY 2 DESC
        """)
    top_five_results = cur.fetchall()[:5]
    industry_label = [x[0] for x in top_five_results]
    mcount = np.array([x[2] for x in top_five_results])
    fcount = np.array([x[3] for x in top_five_results])
    nacount = np.array([x[4] for x in top_five_results])

    fig, ax = plt.subplots(figsize=(16,10))
    bar_width = 0.2
    ind = np.arange(5)
    p1 = plt.bar(ind, mcount, bar_width, color = "blue", label="Male")
    p2 = plt.bar(ind+bar_width, fcount, bar_width, color = "orange", label="Female")
    p3 = plt.bar(ind+2*bar_width, nacount, bar_width, color = "green", label="N/A")

    plt.xlabel('Industry')
    plt.ylabel('Number of People on Forbes 400 List')
    plt.title('Count of Forbes 400 by Top 5 Industries and Gender')

    plt.xticks(ind + bar_width, (industry_label[0], industry_label[1],industry_label[2], industry_label[3],industry_label[4]))
    plt.legend()
    plt.tight_layout()
    plt.savefig('IndustryCounts.png')
    #plt.show()

#4. Scatter plot: Number of Forbes 400 Billionaires vs Gini Coef of Country
def graph_gini_vs_number_billionaires(cur, conn):
    sql = """
    SELECT f.country_id, c.gini_percent
        FROM ForbesPeople f
        INNER JOIN CountryWealth c on c.key = f.country_id
    """

    results = cur.execute(sql).fetchall()

    country_counts = {}
    for item in results:
        if item[0]!= None and item[0] not in country_counts:
            country_counts[item[0]] = 0
        country_counts[item[0]] += 1

    keys = []
    gini = []
    counts = []
    for item in results:
        key = item[0]
        gini_pct = item[1]
        count = country_counts[key]

        if key not in keys:
            keys.append(key)
            gini.append(gini_pct)
            counts.append(count)

    fig, ax = plt.subplots(figsize=(16,10))

    ax.scatter(gini, counts)

    ax.set_xlabel('Gini Percentage')
    ax.set_ylabel('Count of Individuals on Forbes 400 List')
    ax.set_title("Country's Count of Individuals on Forbes 400 List vs Gini Percentage")

    plt.savefig('GiniCountGraph.png')
    #plt.show()

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

    #Chart 1
    graph_top_100_vs_total_US_wealth(cur, conn)

    #Chart 2
    graph_count_by_country(cur, conn)

    #Chart 3
    graph_count_of_forbes_by_industry(cur, conn)

    #Chart 4
    graph_gini_vs_number_billionaires(cur, conn)

    #Chart 5
    graph_age_vs_net_worth(cur, conn)

main()
