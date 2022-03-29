import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def add_coin_watcher():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    c.execute("SELECT id FROM new_coins")

    rows = c.fetchall()
    print(rows)

    for row in rows:

        i = 0
        coin_id = str(row[i]).replace("-", "_")
        sql_query = ("ALTER TABLE coin_watcher ADD unix_time_" + coin_id + " integer")
        
        c.execute(sql_query)

        sql_query = ("ALTER TABLE coin_watcher ADD " + coin_id + " text")
        
        c.execute(sql_query)

        i += 1

    c.execute("INSERT INTO coins_on_scanner SELECT * FROM new_coins")


    conn.commit()

    conn.close()
