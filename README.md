# Web Scraping

various web scraping project with BeautifulSoup primarily to scrape an Austrian real estate and marketplace webpage called "willhaben"

## Description

The idea originated in my personal need to find current real estate prices and renting fees without scrolling for hours daily through the web.. 
Unfortunately with the output that rents and prices are ever only rising.. 
Nevertheless this tool should help you find current pricing and tracking of them over time. 

## Getting Started

### Dependencies

the program is written in Python 3
```
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
```

you can run the programm from any platform that support pyhton and sqlite3

### Installing

- install the dependencies via pip install
- sqlite3 maybe some db reader application
- some .csv reader for testing functionalities (if needed or interested) 

### Executing program

just run the scraper_willhaben.py
or
scraper_willhaben_rent.py

depending on your interest for buying or renting something

## Help
you can email me if you need anything regarding this repo

## Authors

Patrick Stampler

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* the programm ist definitely inspired by some project I found on the and I give credits where needed. But I am still searching for the source to mention it here.

