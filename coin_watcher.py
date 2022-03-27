import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def add_coin_watcher():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # c.execute("INSERT OR IGNORE INTO wallet(id, address, unix_time, timestamp) SELECT id, address, unix_time, timestamp FROM new_coins")

    c.execute("SELECT symbol FROM new_coins")

    rows = c.fetchall()
    print(rows)

    for row in rows:
        print(row)
        i = 0
        # c.execute("UPDATE wallet SET amount = ? WHERE address = ?",(float(balance), str(row[i]),))
        print(str(row[i]))
        # c.execute("ALTER TABLE coin_watcher ADD @row[i] (?) text",(str(row[i])))
        sql_query = ("ALTER TABLE coin_watcher ADD " + str(row[i]) + " text")
        print(sql_query)
        c.execute(sql_query)

        i += 1



    # current_time = datetime.now()
    # unix_time = datetime.timestamp(current_time) - 600
    # # c.execute("DELETE FROM wallet WHERE address IS NULL OR address = ''")
    # c.execute("DELETE FROM wallet WHERE unix_time < :unix_time AND amount = 0",{'unix_time': unix_time})

    conn.commit()

    conn.close()
