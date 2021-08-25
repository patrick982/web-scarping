from os import error
from sqlite3.dbapi2 import Connection, Cursor, Date, connect
from bs4 import BeautifulSoup
import urllib.request
import re
import sqlite3
import csv
import time
from datetime import datetime
from datetime import date


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
    time.sleep(1)
    soupString = str(soup)

    post_code = re.search('post_code":"(.*?)"', soupString)
    price = re.search('price":"(.*?)"', soupString)
    rooms = re.search('rooms":"(.*?)"', soupString)
    timestamp = datetime.now()
    date = Date.today()

    print("This is apartment in " + post_code.group(1) + ", with " +
          rooms.group(1) + " rooms, price is " + price.group(1) + "." + " " + url)

    return post_code.group(1), price.group(1), rooms.group(1), timestamp, date


graz_apartment_links = []

for i in range(1, 4):
    fp = urllib.request.urlopen(
        "https://www.willhaben.at/iad/immobilien/eigentumswohnung/eigentumswohnung-angebote?rows=5&sfId=d4217f20-4c20-4a19-9637-716224555df5&parent_areaid=6&areaId=601&isNavigation=true&NO_OF_ROOMS_BUCKET=4X4&page=" + str(i))

    mybytes = fp.read()
    mystr = mybytes.decode("ISO-8859-1")
    fp.close()

    soup = BeautifulSoup(mystr, 'html.parser')
    time.sleep(1)

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
        try:
            post_code, price, rooms, timestamp, date = get_apartment_details(
                url)
            combined = post_code + ',' + price + ',' + rooms + ',' + url
            writer.writerow([combined])
            count = cursor.execute("INSERT INTO immobuy(zip, price, rooms, url, timestamp, date) VALUES(?,?,?,?,?,?)", (
                post_code, price, rooms, url, timestamp, date))
            db.commit()
        except:
            continue

# close file
f.close()
