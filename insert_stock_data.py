__author__ = 'tomtomssi'
import urllib.request

import psycopg2
from bs4 import BeautifulSoup as Soup


def query_for_abbreviations():
    conn_string = "host='localhost' dbname='stock' user='xx' password='xx'"

    connection = psycopg2.connect(conn_string)

    cursor = connection.cursor()

    cursor.execute("SELECT * from abbreviations ORDER BY name")

    query_for_data(connection, cursor)


def get_stock_data(abbreviation):
    html = urllib.request.urlopen("http://eoddata.com/stockquote/NYSE/" + abbreviation + ".htm")
    soup = Soup(html, "html.parser")
    price = soup.find("b", {"style": "color:red;font-size:26px"})
    table = soup.find("table", {"class": "rc_t"})
    name = table.findAll("td")
    return name[1].contents[0]


def query_for_data(connection, cursor):
    for item in cursor.fetchall():
        print("INSERT INTO data(name, abbreviation_key) "
                       "VALUES (%s, %s)", [get_stock_data(item[0]), item[1]])

        cursor.execute("INSERT INTO data(name, abbreviation_key) "
                       "VALUES (%s, %s)", [get_stock_data(item[0]), item[1]])
        connection.commit()

query_for_abbreviations()

