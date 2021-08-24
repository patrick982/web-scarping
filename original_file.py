from bs4 import BeautifulSoup
import urllib.request
import re
import requests


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
              rooms.group(1) + " rooms, price is " + price.group(1) + ".")
    except AttributeError:
        print("x")

    print(url)


graz_apartment_links = []
page_count = 1

for i in range(1, 4):

    fp = requests.get(
        "https://www.willhaben.at/iad/immobilien/eigentumswohnung/steiermark/graz/?rows=5&page=" + str(page_count))

    page_count += 1

    soup = BeautifulSoup(fp.content, "html.parser")
    # print(soup.find_all('a'))

    for link in soup.find_all('a'):
        url = link.get('href')

        if url != "#" and url != None and url.startswith(("/iad/immobilien/d/eigentumswohnung/steiermark/graz/")):
            graz_apartment_links.append("https://www.willhaben.at" + url)

    for url in graz_apartment_links:
        get_apartment_details(url)
