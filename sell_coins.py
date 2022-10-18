# From here is sell_coins.js script called until there are no coins left in table
# sell_coins script shouldn't be called from here until there are no coins left because that can loop
# one coin and fuck up all the other coins. Instead the coin should be left in table and examined while
# other coins are sold.
import sqlite3

def delete_sell_coins():

    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    # if the transaction succeeds then delete it from sell coins
    c.execute("DELETE FROM sell_coins WHERE status = ?", (1,))

    conn.commit()

    conn.close()
