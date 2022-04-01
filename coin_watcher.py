import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def add_coin_watcher():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time)    

    c.execute("INSERT INTO coin_watcher(unix_time) VALUES(:unix_time)",{'unix_time': unix_time})


    conn.commit()

    conn.close()
