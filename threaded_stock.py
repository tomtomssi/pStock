import urllib.request
import time
import threading
from queue import Queue

import psycopg2
from bs4 import BeautifulSoup as Soup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
lock = threading.Lock()
q = Queue()

def getStockAbbreviations(letter):
    letter = letter.upper()

    urlString = "http://eoddata.com/stocklist/NYSE/" + letter + ".htm"

    print("Downloading by abbreviation " + letter)

    start_time = time.time()
    html = urllib.request.urlopen(urlString)
    print("Finished in: " + str(time.time() - start_time))
    getHeaderData(html)

    file = formatFile(letter)

    parseHtml(html, file)

    file.close()


def query_database(content):

    conn_string = "host='localhost' dbname='stock' user='xx' password='xx'"

    print("Connecting to database\n	->%s" % (conn_string))

    connection = psycopg2.connect(conn_string)

    cursor = connection.cursor()
    print('Inserting value "%s" into the database...', content)

    cursor.execute("INSERT INTO abbreviations (name) VALUES(%s)", [content])
    connection.commit()

    connection.close()


def formatFile(letter):
    file = open("abbreviations/stock_abb_" + letter + ".txt", "w")
    file.seek(0)
    file.truncate()
    return file


def getHeaderData(html):
    print("Content size: " + html.headers["content-length"])


def parseHtml(html, file):
    soup = Soup(html, "html.parser")
    data = soup.find("table", {"class" : "quotes"})
    for item in data.findAll('a'):
        content = str(item.contents[0])
        if "img" in content:
            continue
        else:
            query_database(content)


def worker():
    while True:
        item = q.get()
        getStockAbbreviations(item)
        q.task_done()

for i in range(5):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

start = time.perf_counter()

for letter in letters:
    q.put(letter)

q.join()

print('time:', time.perf_counter() - start)

