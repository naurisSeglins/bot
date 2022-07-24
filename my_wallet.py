from decimal import Decimal
import sqlite3
import requests
import json
from datetime import datetime

def updating_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # copy coins from new coins to wallet
    # instead of copying all the new coins the new_coins.py script will copy coins from new_coins table to wallet table only the coins
    # that are actually bought
    # c.execute("INSERT OR IGNORE INTO wallet(id, address, timestamp, unix_time) SELECT id, address, timestamp, unix_time FROM new_coins")


    # check how many coins per address I have
    c.execute("SELECT address FROM wallet")
    rows = c.fetchall()

    for row in rows:
        wallet_url = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={}&address=0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59&tag=latest&apikey=TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"
        
        address = requests.get(wallet_url.format(*row, sep='')).text
        address = json.loads(address)
        try:
            balance = Decimal(address["result"]) / (10**18)
        except:
            print("there was error")
            print("for this row ", row)
            print(address)
            print(address["result"])
        
        i = 0
        # update how many coins per address I have
        c.execute("UPDATE wallet SET amount = ? WHERE address = ?",(float(balance), str(row[i]),))
        i += 1


    # saving last round percentage for bnb
    c.execute("SELECT percent_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        # try:
            if data[0]:
                c.execute("UPDATE wallet SET last_percent_bnb = ? WHERE address = ?", (data[0], data[1]))
        # except:
        #     "there was this error here"


    # calculating percentage growth or drop for coins in BNB
    c.execute("SELECT bnb_price, first_price_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        try:
            if data[0]:
                # updating the first_price of new coin in wallet once
                c.execute("UPDATE OR IGNORE wallet SET first_price_bnb = ? WHERE address = ? AND first_price_bnb IS NULL",(data[0], data[2],))

                # calculating percentage
                real_price = float(data[0])
                first_price = float(data[1])
                growth_perct = round(real_price / first_price * 100, 2)
                c.execute("UPDATE wallet SET percent_bnb = ? WHERE address = ?", (growth_perct, data[2]))
        except:
            print(data)
            print("there was error at wallet_2")


    # saving highest percentage for bnb recorded
    c.execute("SELECT percent_bnb, highest_percent_bnb, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        # try:
        if data[0]:
            if data[1] == None:
                c.execute("UPDATE wallet SET highest_percent_bnb = ? WHERE address = ?", (data[0], data[2],))
            elif data[0] > data[1]:
                c.execute("UPDATE wallet SET highest_percent_bnb = ? WHERE address = ?", (data[0], data[2],))
        # except:
        #     "there was this error here"


    # deleting coins that don't have any amount in wallet
    # after new changes this script will be useless because there won't be coins in wallet that don't have amount
    # except there might be situations when a coin didn't sell all of it's token so if the coin is automatically deleted
    # then it will be lost.
    # Maybe better to leave it in wallet until the amount is 0?
    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 600
    c.execute("DELETE FROM wallet WHERE unix_time < :unix_time AND amount = 0",{'unix_time': unix_time})
    c.execute("UPDATE OR IGNORE wallet SET unix_time = ? WHERE unix_time IS NULL",(unix_time,))

    conn.commit()

    conn.close()


updating_wallet()