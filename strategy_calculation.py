import sqlite3
from datetime import datetime

def short_strategy_calc():

    conn = sqlite3.connect("coins.db")

    c = conn.cursor()
    # !!!!!!!!!!!!!!!!! SHORT !!!!!!!!!!!!!!!!!


    # calculation short coin strategy fake buying
    c.execute("SELECT percent_bnb, first_percent_bnb, address FROM new_coins")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            if data[0] - data[1] >= 5:
                c.execute("INSERT OR IGNORE INTO strategy_short(id, address, percent_bnb, last_percent_bnb, first_percent_bnb) SELECT (id, address, percent_bnb, last_percent_bnb, first_percent_bnb) FROM new_coins WHERE address = ?", (data[2],))

    # update price if the coin isn't fake sold

    # fake sell coin

    conn.commit()

    conn.close()
