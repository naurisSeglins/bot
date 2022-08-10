# From here is sell_coins.js script called until there are no coins left in table
# sell_coins script shouldn't be called from here until there are no coins left because that can loop
# one coin and fuck up all the other coins. Instead the coin should be left in table and examined while
# other coins are sold.
import sqlite3
from datetime import datetime

def decimal_fixing():

    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    c.execute("SELECT address, status, decimal FROM sell_coins")
    coin_data = c.fetchall()


    # if the transaction fails and decimal is 18 change it to 9
    for data in coin_data:
            if data[1]:
                if data[1] == 0 and data[2] == 18:
                    c.execute("UPDATE sell_coins SET decimal = ? WHERE address = ?", (9, data[0]))


    # if the transaction succeeds then delete it from sell coins
    c.execute("DELETE FROM sell_coins WHERE status = ?", (1))

    conn.commit()

    conn.close()