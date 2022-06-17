import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def checking_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # copy coins from new coins to wallet
    c.execute("INSERT OR IGNORE INTO wallet(id, address, timestamp, unix_time) SELECT id, address, timestamp, unix_time FROM new_coins")

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


    # saving last round percentage for busd and bnb
    c.execute("SELECT percent_bnb, percent_busd, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        # try:
            if data[0]:
                c.execute("UPDATE wallet SET last_percent_bnb = ? WHERE address = ?", (data[0], data[2]))
            if data[1]:
                c.execute("UPDATE wallet SET last_percent_busd = ? WHERE address = ?", (data[1], data[2]))
        # except:
        #     "there was this error here"


    # getting the price of BUSD to convert later prices from BNB to BUSD
    c.execute("SELECT bnb_price, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        try:
            if data[1] == "0xe9e7cea3dedca5984780bafc599bd69add087d56":
                busd_price = data[0] / 3
        except:
            "there was error_2"


    # calculating percentage growth or drop for coins in BUSD
    c.execute("SELECT bnb_price, first_price_busd, address, busd_price FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        try:
            if data[0]:
                # converting coins from BNB to BUSD
                bnb_to_busd = data[0] / busd_price
                c.execute("UPDATE wallet SET busd_price = ? WHERE address = ?", (bnb_to_busd, data[2]))

                # updating the first_price of new coin in wallet once
                c.execute("UPDATE OR IGNORE wallet SET first_price_busd = ? WHERE address = ? AND first_price_busd IS NULL",(bnb_to_busd, data[2],))

                # calculating percentage
                real_price = float(data[3])
                first_price = float(data[1])
                growth_perct = round(real_price / first_price * 100, 2)
                c.execute("UPDATE wallet SET percent_busd = ? WHERE address = ?", (growth_perct, data[2]))
        except:
            print("there was error at wallet_1")
            print(data[0])


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


    # saving last round percentage for busd and bnb
    c.execute("SELECT percent_bnb, percent_busd, high_percent_bnb, high_percent_busd, address FROM wallet")
    coin_data = c.fetchall()

    for data in coin_data:
        # try:
        if data[0]:
            print(data[0])
            print(data[2])
            if data[2] == None:
                c.execute("UPDATE wallet SET high_percent_bnb = ? WHERE address = ?", (data[0], data[4],))
            elif data[0] > data[2]:
                c.execute("UPDATE wallet SET high_percent_bnb = ? WHERE address = ?", (data[0], data[4],))
        if data[1]:
            print(data[1])
            print(data[3])
            if data[3] == None:
                c.execute("UPDATE wallet SET high_percent_busd = ? WHERE address = ?", (data[1], data[4],))
            elif data[1] > data[3]:
                c.execute("UPDATE wallet SET high_percent_busd = ? WHERE address = ?", (data[1], data[4],))
        # except:
        #     "there was this error here"

    # deleting coins that don't have any amount in wallet
    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 600
    c.execute("DELETE FROM wallet WHERE unix_time < :unix_time AND amount = 0",{'unix_time': unix_time})
    c.execute("UPDATE OR IGNORE wallet SET unix_time = ? WHERE unix_time IS NULL",(unix_time,))

    conn.commit()

    conn.close()
