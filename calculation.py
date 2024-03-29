import sqlite3
from datetime import datetime

# here will be calculations when to but and sell coin!

def calculate_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    # !!!!!!!!!!!!!!!!! WALLET !!!!!!!!!!!!!!!!!

    # saving last round percentage for bnb
    c.execute("SELECT percent_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
            if data[0]:
                c.execute("UPDATE wallet SET last_percent_bnb = ? WHERE address = ?", (data[0], data[1],))

    # updating the first_price of new coin in wallet once
    c.execute("SELECT bnb_price, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            # šeit veidojas errors jo pirmo reizi first_price_bnb ir None!
            c.execute("UPDATE OR IGNORE wallet SET first_price_bnb = ? WHERE address = ? AND first_price_bnb IS NULL",(data[0], data[1],))

    conn.commit()

    # calculating percentage growth or drop for coins in BNB
    c.execute("SELECT bnb_price, first_price_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
            if data[0]:
                # calculating percentage
                real_price = float(data[0])
                first_price = float(data[1])
                growth_perct = round(real_price / first_price * 100, 2)
                c.execute("UPDATE wallet SET percent_bnb = ? WHERE address = ?", (growth_perct, data[2],))

    # saving highest percentage for bnb recorded
    c.execute("SELECT percent_bnb, highest_percent_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            if data[1] == None:
                c.execute("UPDATE wallet SET highest_percent_bnb = ? WHERE address = ?", (data[0], data[2],))
            elif data[0] > data[1]:
                c.execute("UPDATE wallet SET highest_percent_bnb = ? WHERE address = ?", (data[0], data[2],))


    # this is calculation to decide if the coin needs to be selled
    c.execute("SELECT percent_bnb, highest_percent_bnb, address FROM wallet")

    rows = c.fetchall()
    current_time = datetime.now()

    for row in rows:
        if row[0]:
            # checking if wallet coin price has gone down for 15%
            if row[1] - row[0] >= 15:
                print("percent bnb = ",row[0])
                print("highest percent bnb = ", row[1])
                address = str(row[2])

                sql_query = ("INSERT OR IGNORE INTO sell_coins(id, address, unix_time, timestamp, amount, decimal) SELECT id, address, unix_time, timestamp, amount, decimal FROM wallet WHERE address = ?")
                c.execute(sql_query, (address,))
                sql_query = ("INSERT OR IGNORE INTO sell_calculation_history SELECT * FROM wallet WHERE address = ?")
                c.execute(sql_query, (address,))

                unix_time = datetime.timestamp(current_time)
                c.execute("UPDATE sell_coins SET unix_time = ? WHERE address = ?",(unix_time, address,))

                # if the price for wallet coin has gone down then delete this coin from wallet table
                sql_query = ("DELETE FROM wallet WHERE address= ?")
                c.execute(sql_query, (address,))
    conn.commit()

    conn.close()



def calculate_new_coins():

    conn = sqlite3.connect("coins.db")

    c = conn.cursor()
    # !!!!!!!!!!!!!!!!! NEW COINS !!!!!!!!!!!!!!!!!


    # saving last round percentage for bnb
    c.execute("SELECT percent_bnb, address FROM new_coins")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            c.execute("UPDATE new_coins SET last_percent_bnb = ? WHERE address = ?", (data[0], data[1],))


   # updating the first_price of new coin in new_coins once
    c.execute("SELECT bnb_price, address FROM new_coins")
    coin_data = c.fetchall()
    for data in coin_data:
        if data[0]:
            c.execute("UPDATE new_coins SET first_price_bnb = ? WHERE address = ? AND first_price_bnb IS NULL",(data[0], data[1],))


    # calculating percentage growth or drop for coins in BNB
    c.execute("SELECT bnb_price, first_price_bnb, address FROM new_coins")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            real_price = float(data[0])
            first_price = float(data[1])
            growth_perct = round(real_price / first_price * 100, 2)
            c.execute("UPDATE new_coins SET percent_bnb = ? WHERE address = ?", (growth_perct, data[2],))


    # saving highest percentage for bnb recorded
    c.execute("SELECT percent_bnb, address FROM new_coins")
    coin_data = c.fetchall()

    for data in coin_data:
        if data[0]:
            c.execute("UPDATE new_coins SET first_percent_bnb = ? WHERE address = ? AND first_percent_bnb IS NULL", (data[0], data[1],))

    # !!!!!!!!!!!!!!!!!!!! until strategy is decided this is commented !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # # this is a calculation to decide if the coin needs to be bought


    conn.commit()

    conn.close()
