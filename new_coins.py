import sqlite3
from datetime import datetime

def move_new_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()



    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 300
    # adding new coins to the new_coins table
    c.execute("INSERT OR IGNORE INTO new_coins(id, symbol, address, unix_time, timestamp) SELECT id, symbol, address, unix_time, timestamp FROM coins WHERE unix_time > :unix_time",{'unix_time': unix_time})
    # deleting new coins that are not BSC 
    c.execute("DELETE FROM new_coins WHERE address IS NULL OR address = ''")
    # deleting new coins after time when they are not new
    # c.execute("DELETE FROM new_coins WHERE unix_time < :unix_time",{'unix_time': unix_time})

    # checking if new coin price has gone up for 10%
    # this checking will be done by script new_coin_price.js that needs to be made similar to script wallet_coin_price.js

    # if the price for new coin has gone up then copy this coin to buy_coins table

    # if the price for new coin has gone up then copy this coin to wallet table

    # if the price for new coin has gone up then delete this coin from new_coins table

    conn.commit()

    conn.close()

