import sqlite3
import requests
import json
from datetime import datetime
import time 

def adding_new_coins_to_db():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    # coin adding to database
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=999&page={}&sparkline=false"

    url_add = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

    i = 1

    while True:
        try:
            data = requests.get(url.format(i)).text
            data = json.loads(data)
        except:
            print("Error at data url!")
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
    time.sleep(5)  # do work every one hour

    # address adding
    index_ok = 0
    while index_ok == 0:

        try:
            address = requests.get(url_add).text
            time.sleep(5)  # do work every one hour
            address = json.loads(address)
            index_ok = 1
        except:
            print("error at first address!")
            print("error at second address!")
        time.sleep(5)  # do work every one hour


    dateTimeObj = datetime.now()
    print("started address adding at: ", dateTimeObj)
    try:
        for ids in address:
            try:
                coin_address = ids["platforms"].get("binance-smart-chain")
                if coin_address:
                    if len(coin_address) < 21:
                        print(ids)
                        continue
                c.execute("UPDATE OR IGNORE coins SET address = :address WHERE id = :id", {'address': coin_address,'id': ids["id"]})
            except:
                print(coin_address[0], coin_address[-1])
                print("error at address update loop")
    except:
        print("error at address adding")

    conn.commit()

    conn.close()