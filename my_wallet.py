import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def checking_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    my_api_key = "TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"

    wallet_url = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x9f28455a82baa6b4923a5e2d7624aaf574182585&address=0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59&tag=latest&apikey=TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"

    address = requests.get(wallet_url).text
    address = json.loads(address)

    print(address)
    print(address["result"])
    balance = Decimal(address["result"]) / (10**18)
    print(balance)
    dateTimeObj = datetime.now()
    print("commiting at: ", dateTimeObj)

    conn.commit()

    conn.close()