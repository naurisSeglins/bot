import sqlite3
from datetime import datetime

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

def clean_new_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    c.execute("DELETE FROM new_coins WHERE got_pair = ?",("0x0000000000000000000000000000000000000000",))

    conn.commit()

    conn.close()
