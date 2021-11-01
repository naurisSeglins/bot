import sqlite3
import requests
import json
from datetime import datetime

def move_some_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 43200
    c.execute("INSERT OR IGNORE INTO new_coins(id, symbol, current_price, market_cap, address, unix_time, timestamp) SELECT id, symbol, current_price, market_cap, address, unix_time, timestamp FROM coins WHERE unix_time > :unix_time",{'unix_time': unix_time})
    c.execute("DELETE FROM new_coins WHERE address IS NULL")
    c.execute("DELETE FROM new_coins WHERE unix_time < :unix_time",{'unix_time': unix_time})

    print(unix_time)
    print(current_time)

    conn.commit()

    conn.close()



move_some_coins()

