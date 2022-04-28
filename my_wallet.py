import sqlite3
import requests
import json
from datetime import datetime
from decimal import Decimal

def checking_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    c.execute("INSERT OR IGNORE INTO wallet(id, address, unix_time, timestamp) SELECT id, address, unix_time, timestamp FROM new_coins")

    c.execute("SELECT address FROM wallet")

    rows = c.fetchall()

    for row in rows:
        wallet_url = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={}&address=0xAeCb376d7484f29143c626a7Aa29C0CD7Ae39e59&tag=latest&apikey=TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"
        
        address = requests.get(wallet_url.format(*row, sep='')).text
        address = json.loads(address)
        balance = Decimal(address["result"]) / (10**18)
        

        i = 0
        c.execute("UPDATE wallet SET amount = ? WHERE address = ?",(float(balance), str(row[i]),))
        i += 1


    current_time = datetime.now()
    unix_time = datetime.timestamp(current_time) - 600
    # c.execute("DELETE FROM wallet WHERE address IS NULL OR address = ''")
    c.execute("DELETE FROM wallet WHERE unix_time < :unix_time AND amount = 0",{'unix_time': unix_time})

    conn.commit()

    conn.close()

















