import sqlite3
import requests
import json

conn = sqlite3.connect("coins.db")

c = conn.cursor()


url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=999&page={}&sparkline=false"

url_add = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

cnt, i = 1, 1
# while True:
#     try:
#         data = requests.get(url.format(i)).text
#         data = json.loads(data)
#     except:
#         print("Error!")
#         break

#     if not data:
#         break

#     for ids in data:
#         print("{:>3}. {}".format(cnt, ids["name"]))
#         c.execute("INSERT OR IGNORE INTO coins(id, symbol, current_price, market_cap) VALUES (?, ?, ?, ?)",
#                   (ids["id"], ids["symbol"], ids["current_price"], ids["market_cap"],))
#         print(ids["id"])
#         cnt += 1
#     i += 1

address = requests.get(url_add).text
address = json.loads(address)

# print(address)

for ids in address:
    print("{:>3}. {}".format(cnt, ids["id"]))
#     c.execute("INSERT OR IGNORE INTO coins(id, symbol, current_price, market_cap) VALUES (?, ?, ?, ?)",
#               (ids["id"], ids["symbol"], ids["current_price"], ids["market_cap"],))
    print(ids["platforms"])
    cnt += 1

conn.commit()

conn.close()
