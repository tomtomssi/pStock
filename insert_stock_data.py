__author__ = 'tomtomssi'
import urllib.request
import time
import threading
from queue import Queue

import psycopg2
from bs4 import BeautifulSoup as Soup

import config_parser

lock = threading.Lock()
q = Queue()


def query_for_abbreviations():
    config = config_parser.ParseConfig()

    conn_string = "host='{0}'dbname='{1}'user='{2}'password='{3}'".format(config.get_host(), config.get_database(), config.get_username(), config.get_password())

    connection = psycopg2.connect(conn_string)

    cursor = connection.cursor()

    cursor.execute("SELECT * from abbreviations ORDER BY name")

    data = cursor.fetchall()

    connection.close()

    return data


def get_stock_data(abbreviation):
    html = urllib.request.urlopen("http://eoddata.com/stockquote/NYSE/" + abbreviation + ".htm")
    soup = Soup(html, "html.parser")
    price = soup.find("b", {"style": "color:red;font-size:26px"})
    table = soup.find("table", {"class": "rc_t"})
    name = table.findAll("td")
    return name[1].contents[0]


def query_for_data(item):
    config = config_parser.ParseConfig()

    conn_string = "host='{0}'dbname='{1}'user='{2}'password='{3}'".format(config.get_host(), config.get_database(), config.get_username(), config.get_password())

    connection = psycopg2.connect(conn_string)

    cursor = connection.cursor()

    print("INSERT INTO data(name, abbreviation_key) "
                   "VALUES (%s, %s)", [get_stock_data(item[0]), item[1]])

    cursor.execute("INSERT INTO data(name, abbreviation_key) "
                   "VALUES (%s, %s)", [get_stock_data(item[0]), item[1]])

    connection.commit()

    connection.close()


def worker():
    while True:
        item = q.get()
        query_for_data(item)
        q.task_done()


for i in range(5):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

start = time.perf_counter()

for abbreviation in query_for_abbreviations():
    q.put(abbreviation)

q.join()

print('time:', time.perf_counter() - start)

