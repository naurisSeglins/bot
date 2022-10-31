import sqlite3
from datetime import datetime
import requests
import json


def move_new_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    current_time = datetime.now()
    # inserting into new_coins table from coins table if coin is within 30 sec young (30sec)
    unix_time = datetime.timestamp(current_time) - 30
    # adding new coins to the new_coins table
    c.execute("INSERT OR IGNORE INTO new_coins(id, symbol, address, unix_time, timestamp) SELECT id, symbol, address, unix_time, timestamp FROM coins WHERE unix_time > :unix_time",{'unix_time': unix_time})
    # deleting new coins that are not BSC 
    c.execute("DELETE FROM new_coins WHERE address IS NULL OR address = ''")

    # deleting new coins after time when they are not new
    # c.execute("DELETE FROM new_coins WHERE unix_time < :unix_time",{'unix_time': unix_time})

    conn.commit()

    conn.close()

    # calling decimal function
    add_decimal()

def add_decimal():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # check how many decimals the coin has
    c.execute("SELECT id, decimal, address FROM new_coins")
    allData = c.fetchall()

    for data in allData:

        if data[1] == None:
            wallet_url = f"https://api.coingecko.com/api/v3/coins/{data[0]}"
            decimals = requests.get(wallet_url).text
            decimals = json.loads(decimals)
            try:
                decimals = decimals["detail_platforms"].get("binance-smart-chain")
                coinDecimals = decimals.get("decimal_place")
            except:
                print("there was error")
                print("for this row ", data)
            
            c.execute("UPDATE new_coins SET decimal = ? WHERE address = ?",(coinDecimals, str(data[2]),))

    conn.commit()
    conn.close()

def clean_new_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    c.execute("DELETE FROM new_coins WHERE got_pair = ?",("0x0000000000000000000000000000000000000000",))

    conn.commit()

    conn.close()



# Traceback (most recent call last):
#   File "/home/bot/Desktop/bot/bot/main.py", line 38, in <module>
#     move_new_coins()
#   File "/home/bot/Desktop/bot/bot/new_coins.py", line 28, in move_new_coins
#     add_decimal()
#   File "/home/bot/Desktop/bot/bot/new_coins.py", line 44, in add_decimal
#     decimals = json.loads(decimals)
#   File "/usr/lib/python3.9/json/__init__.py", line 346, in loads
#     return _default_decoder.decode(s)
#   File "/usr/lib/python3.9/json/decoder.py", line 337, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#   File "/usr/lib/python3.9/json/decoder.py", line 355, in raw_decode
#     raise JSONDecodeError("Expecting value", s, err.value) from None
