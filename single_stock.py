__author__ = 'tomtomssi'

import urllib.request
import re

from bs4 import BeautifulSoup as Soup

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
           'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def findFile(letter):
    return open("stock_abb_" + letter + ".txt")


def do_work(letter):
    for file_line in open("stock_abb_" + letter + ".txt").readlines():
        html = urllib.request.urlopen("http://www.reuters.com/finance/stocks/overview?symbol=" + file_line)
        soup = Soup(html, "html.parser")
        for line in soup.findAll("div", {"id": "headerQuoteContainer"}):
            file = open("single_stock/stock_" + letter + ".txt", "w")
            number = str(line.findAll("span")[1].contents[0])
            file.write(file_line + ": " + re.findall(r'\d+\.*\d*', number)[0])
            file.close()

do_work('A')
