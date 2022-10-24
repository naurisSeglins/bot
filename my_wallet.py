from decimal import Decimal
import sqlite3
import requests
import json
from datetime import datetime
def cutting(x):
    # print(x)
    numbers = 0
    second_part = ""
    two_parts = x.split(".")
    if len(two_parts) == 2:
        for char in two_parts[1]:
            second_part += char
            if char != "0":
                numbers +=1
            if numbers == 3:
                break
            if second_part == "000" and two_parts[0] != "0":
                break
    if second_part == "000" or second_part == "":
        result = two_parts[0]
    else:
        result = two_parts[0] + "."+ second_part
    # print(result)
    return result

def updating_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    # check how many coins per address I have
    c.execute("SELECT address, decimal FROM wallet")
    rows = c.fetchall()

    for row in rows:
        wallet_url = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={}&address=0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59&tag=latest&apikey=TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"
        
        address = requests.get(wallet_url.format(*row, sep='')).text
        address = json.loads(address)
        try:
            balance = Decimal(address["result"]) / (10**row[1])

        except:
            print("there was error")
            print("for this row ", row)
            print(address)
            print(address["result"])
        # strip unnecessary decimals
        stripedBalance = cutting(str(balance))
        c.execute("INSERT OR IGNORE INTO amount_conversion(id, original, converted) VALUES(?,?,?)", (str(row[0]), float(balance), float(stripedBalance),))
        
        # update how many coins per address I have
        c.execute("UPDATE wallet SET amount = ? WHERE address = ?",(float(stripedBalance), str(row[0]),))

    
    # if there is amount for coin in wallet then delete this coin from buy coins
    c.execute("SELECT address, amount FROM wallet")
    rows = c.fetchall()
    
    for row in rows:
        if row[1]:
            c.execute("DELETE FROM buy_coins WHERE address = ?", (str(row[0]),))


    # updating unix time if there is no unix time
    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 600
    c.execute("UPDATE OR IGNORE wallet SET unix_time = ? WHERE unix_time IS NULL",(unix_time,))


    conn.commit()

    conn.close()
