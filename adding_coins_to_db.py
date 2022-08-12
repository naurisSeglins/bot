import sqlite3
import requests
import json
from datetime import datetime
import time 

def adding_new_coins_to_db():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    # url
    url_add = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

    # request
    try:
        data = requests.get(url_add).text
        time.sleep(5)
        data = json.loads(data)
    except:
        print("error at first address!")
    time.sleep(5)


    # adding coins to the db
    dateTimeObj = datetime.now()
    print("started coin adding at: ", dateTimeObj)
    for ids in data:
        try:
            current_time = datetime.now()
            unix_time = datetime.timestamp(current_time)
            c.execute("INSERT OR IGNORE INTO coins(id, symbol, unix_time) VALUES (?, ?, ?)",
                    (ids["id"], ids["symbol"], unix_time,))   
        except:
            print(coin_address[0], coin_address[-1])
            print("error at address update loop")


    # request
    try:
        address = requests.get(url_add).text
        time.sleep(5)
        address = json.loads(address)
    except:
        print("error at second address!")
    time.sleep(5)


    # adding addreses to the coins
    dateTimeObj = datetime.now()
    print("started address adding at: ", dateTimeObj)
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


    conn.commit()

    conn.close()
