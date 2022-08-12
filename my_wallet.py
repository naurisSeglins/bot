from decimal import Decimal
import sqlite3
import requests
import json
from datetime import datetime
import numpy as np

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
            # there is still issue with super small numbers because they can't be converted to normal float they cannot be selled 
            # for example 5.85914746284e-7
            # this issue is connected to the problem that not all coins are sold but little tiny bits are left
            # print("old format: ", balance)
            # balance = np.format_float_positional(float(address["result"]), trim='-')
            # print("old new format: ", balance)
        except:
            print("there was error")
            print("for this row ", row)
            print(address)
            print(address["result"])
        
        i = 0
        # update how many coins per address I have
        c.execute("UPDATE wallet SET amount = ? WHERE address = ?",(float(balance), str(row[i]),))
        i += 1


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