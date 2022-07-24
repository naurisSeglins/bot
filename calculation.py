import sqlite3
from datetime import datetime

# here will be calculations when to but and sell coin!

def calculate():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()
    # why is all deleted from sell coins?
    # so that the selled coins wouldn't be sold again!
    # taking this script part to sell_coins.py script.
    # c.execute("DELETE FROM sell_coins")

    # this is calculation to decide if the coin needs to be selled
    c.execute("SELECT percent_bnb, highest_percent_bnb, address FROM wallet")

    rows = c.fetchall()
    current_time = datetime.now()

    for row in rows:
        if row[0]:
            if row[1] - row[0] >= 10:
                print("percent bnb = ",row[0])
                print("highest percent bnb = ", row[1])
                address = str(row[2])

                sql_query = ("INSERT INTO sell_coins SELECT id, address, unix_time, timestamp, amount FROM wallet WHERE address = ?")
                c.execute(sql_query, (address,))

                unix_time = datetime.timestamp(current_time)
                c.execute("UPDATE sell_coins SET unix_time = ? WHERE address = ?",(unix_time, address,))

    # this is a calculation to decide if the coin needs to be bought



    conn.commit()

    conn.close()