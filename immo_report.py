import sqlite3
import pandas as pd

# connect to database
con = sqlite3.connect("scraper_data.db")
cur = con.cursor()

# print the result for test
for row in cur.execute("SELECT * FROM immorent;"):
    print(row)
