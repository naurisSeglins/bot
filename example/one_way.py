import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def add_column():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # last column digit?
    sql = "PRAGMA table_info(coin_watcher);"

    c.execute(sql)

    rows = c.fetchall()

    last_column_name = rows[-1][1]
    print(last_column_name)
    last_column_digits = last_column_name.split("_")[1]
    print(last_column_digits)
    last_column_digits = int(last_column_digits) + 1
    print(last_column_digits)


    # in here a new column with a number is added to the coin_watcher table
    sql_query = ("ALTER TABLE coin_watcher ADD nr_" + last_column_digits + " integer")
    
    c.execute(sql_query)

    conn.commit()

    conn.close()

add_column()