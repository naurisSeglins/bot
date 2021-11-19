import sqlite3
import requests
import json
from datetime import datetime
import time 

def do_some_work():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=999&page={}&sparkline=false"

    url_add = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

    i = 1

    while True:
        try:
            data = requests.get(url.format(i)).text
            data = json.loads(data)
        except:
            print("Error at data url!")
            print(data)
            break

        if not data:
            break

        for ids in data:
            try:
                current_time = datetime.now()
                unix_time = datetime.timestamp(current_time)
                c.execute("INSERT OR IGNORE INTO coins(id, symbol, unix_time) VALUES (?, ?, ?)",
                        (ids["id"], ids["symbol"], unix_time,))                
            except:
                print("Error at inserting coins!")
                print(ids)
                break

        i += 1

    try:
        address = requests.get(url_add).text
    except:
        print("error at first address!")
    
    time.sleep(5)  # do work every one hour

    try:
        address = json.loads(address)
    except:
        print("error at second address!")
        print(address)

    try:
        dateTimeObj = datetime.now()
        print("started address adding at: ", dateTimeObj)
    except:
        print("error at address time!")

    for ids in address:
        try:
            c.execute("UPDATE OR IGNORE coins SET address = :address WHERE id = :id", {'address': ids["platforms"].get("binance-smart-chain"),'id': ids["id"]})
        except:
            print("error at address update loop")

    conn.commit()

    conn.close()