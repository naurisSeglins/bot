import sqlite3
import requests
import json
from datetime import datetime

def checking_wallet():
    conn = sqlite3.connect("coins.db")

    c = conn.cursor() 

    my_api_key = "TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"

    wallet_url = "https://api.bscscan.com/api?module=stats&action=tokenCsupply&contractaddress=0xD0E9e6Fee8c8CD46787353d46E067EB663b76F0D&apikey=TU1KAW3FWN3QG3EJBM23DZ5HF3CB8SEF5Z"

    address = requests.get(wallet_url).text
    address = json.loads(address)

    print(address)

    dateTimeObj = datetime.now()
    print("commiting at: ", dateTimeObj)

    conn.commit()

    conn.close()