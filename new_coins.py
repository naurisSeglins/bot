import sqlite3
from datetime import datetime
import requests
import json


def move_new_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    current_time = datetime.now()
    # inserting into new_coins table from coins table if coin is within 180 sec young (3mins)
    unix_time = datetime.timestamp(current_time) - 180
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
