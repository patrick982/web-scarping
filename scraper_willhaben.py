from os import error
from sqlite3.dbapi2 import Connection, Cursor, connect
from bs4 import BeautifulSoup
import urllib.request
import re
import sqlite3
import csv


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except error as e:
        print(e)

    return conn


def get_apartment_details(url):
    fp = urllib.request.urlopen(url)

    mybytes = fp.read()
    mystr = mybytes.decode("ISO-8859-1")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')
    soupString = str(soup)

    post_code = re.search('post_code":"(.*?)"', soupString)
    price = re.search('price":"(.*?)"', soupString)
    rooms = re.search('rooms":"(.*?)"', soupString)

    try:
        print("This is apartment in " + post_code.group(1) + ", with " +
              rooms.group(1) + " rooms, price is " + price.group(1) + "." + url)
    except AttributeError:
        print("x")

    return post_code.group(1), price.group(1), rooms.group(1)


graz_apartment_links = []

page_count = 1

for i in range(1, 4):
    fp = urllib.request.urlopen(
        "https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?&rows=100&areaId=601&parent_areaid=6")

    mybytes = fp.read()
    mystr = mybytes.decode("ISO-8859-1")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')

    for link in soup.find_all('a'):
        url = link.get('href')

        if url != "#" and url != None and url.startswith(("/iad/immobilien/d/eigentumswohnung/steiermark/graz/")):
            graz_apartment_links.append("https://www.willhaben.at" + url)

    # write also to csv
    f = open('csv_test.csv', 'w', newline='')
    writer = csv.writer(f)

    # write also in sqlite db
    db = create_connection('scraper_data.db')
    cursor = db.cursor()

    for url in graz_apartment_links:
        post_code, price, rooms = get_apartment_details(url)
        combined = post_code + ',' + price + ',' + rooms + ',' + url
        writer.writerow([combined])
        count = cursor.execute("INSERT INTO immobuy(zip, price, rooms, url) VALUES(?,?,?,?)", (
            post_code, price, rooms, url))
        db.commit()

# close file
f.close()
