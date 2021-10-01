import json
import requests

url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=eur&order=market_cap_desc&per_page=999&page={}&sparkline=false"

cnt, i = 1, 1
while True:
    try:
        data = requests.get(url.format(i)).text
        data = json.loads(data)
    except:
        print("Error!")
        break

    if not data:
        break

    for d in data:
        print("{:>3}. {}".format(cnt, d["name"]))
        cnt += 1
    i += 1
