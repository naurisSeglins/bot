import sqlite3
from datetime import datetime

def calculate():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    c.execute("SELECT percent_bnb, high_percent_bnb FROM wallet")

    rows = c.fetchall()
    print(rows)

    for row in rows:
        if row[0]:

            print("percent bnb = ",row[0])
            print("highest percent bnb = ", row[1])
            if row[2] - row[1] >= 10:

                sql_query = ("INSERT INTO sell_coins SELECT id, address, unix_time, timestamp, amount FROM wallet")
                c.execute(sql_query)

    conn.commit()

    conn.close()