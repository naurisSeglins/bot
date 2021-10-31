import sqlite3

conn = sqlite3.connect("coins.db")

c = conn.cursor()

c.execute(""" CREATE TABLE coins (
    id text PRIMARY KEY,
    symbol text,
    current_price integer,
    market_cap integer,
    address text,
    unix_time integer,
    timestamp DATE DEFAULT (datetime('now','localtime'))
) """)
# c.execute(""" CREATE TABLE coins_test (
#     id text PRIMARY KEY,
#     symbol text,
#     current_price integer,
#     market_cap integer,
#     address text,
#     timestamp DATE DEFAULT (datetime('now','localtime'))
# ) """)


conn.commit()

conn.close()
