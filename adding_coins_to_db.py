import sqlite3
import requests
import json
import time 
from datetime import datetime

def do_some_work():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()


    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=999&page={}&sparkline=false"

    url_add = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

    cnt, i = 1, 1

    dateTimeObj = datetime.now()
    print("started coin adding at: ", dateTimeObj)

    while True:
        try:
            data = requests.get(url.format(i)).text
            data = json.loads(data)
        except:
            print("Error!")
            break

        if not data:
            break

        for ids in data:
            # print("{:>3}. {}".format(cnt, ids["name"]))
            c.execute("INSERT OR IGNORE INTO coins(id, symbol, current_price, market_cap) VALUES (?, ?, ?, ?)",
                    (ids["id"], ids["symbol"], ids["current_price"], ids["market_cap"],))
            # print(ids["id"])
            cnt += 1
        i += 1

    dateTimeObj = datetime.now()
    print("finished coin adding at: ", dateTimeObj)



    address = requests.get(url_add).text
    address = json.loads(address)

    dateTimeObj = datetime.now()
    print("started address adding at: ", dateTimeObj)


    for ids in address:

        # print("{:>3}. {}".format(cnt, ids["id"]))

        c.execute("UPDATE OR IGNORE coins SET address = :address WHERE id = :id", {'address': ids["platforms"].get("binance-smart-chain"),'id': ids["id"]})
        # print(ids["platforms"].get("binance-smart-chain", ""))

        cnt += 1

    dateTimeObj = datetime.now()
    print("finished address adding at: ", dateTimeObj)

    dateTimeObj = datetime.now()
    print("commiting at: ", dateTimeObj)

    conn.commit()

    conn.close()

if __name__ == "__main__":

    dateTimeObj = datetime.now()
    print("first time at: ", dateTimeObj)

    time.sleep(60)  # imagine you would like to start work in 1 minute first time
    while True:

        dateTimeObj = datetime.now()
        print("doing the work at: ", dateTimeObj)

        do_some_work()

        dateTimeObj = datetime.now()
        print("sleeping for 20 minutes at: ", dateTimeObj)

        time.sleep(1200)  # do work every one hour

        dateTimeObj = datetime.now()
        print("slept for 20 minutes at: ", dateTimeObj)

        