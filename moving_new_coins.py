import sqlite3
from datetime import datetime

def move_some_coins():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()



    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 600
    c.execute("INSERT OR IGNORE INTO new_coins(id, symbol, address, unix_time, timestamp) SELECT id, symbol, address, unix_time, timestamp FROM coins WHERE unix_time > :unix_time",{'unix_time': unix_time})
    c.execute("DELETE FROM new_coins WHERE address IS NULL OR address = ''")
    c.execute("DELETE FROM new_coins WHERE unix_time < :unix_time",{'unix_time': unix_time})

    conn.commit()

    conn.close()

