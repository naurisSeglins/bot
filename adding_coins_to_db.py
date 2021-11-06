import sqlite3
import requests
import json
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
            current_time = datetime.now()
            unix_time = datetime.timestamp(current_time)
            c.execute("INSERT OR IGNORE INTO coins(id, symbol, current_price, market_cap, unix_time) VALUES (?, ?, ?, ?, ?)",
                    (ids["id"], ids["symbol"], ids["current_price"], ids["market_cap"], unix_time,))
            cnt += 1
        i += 1

    dateTimeObj = datetime.now()
    print("finished coin adding at: ", dateTimeObj)



    address = requests.get(url_add).text
    address = json.loads(address)

    dateTimeObj = datetime.now()
    print("started address adding at: ", dateTimeObj)


    for ids in address:


        c.execute("UPDATE OR IGNORE coins SET address = :address WHERE id = :id", {'address': ids["platforms"].get("binance-smart-chain", ""),'id': ids["id"]})

        cnt += 1

    dateTimeObj = datetime.now()
    print("commiting at: ", dateTimeObj)

    conn.commit()

    conn.close()