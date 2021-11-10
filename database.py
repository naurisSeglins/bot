import sqlite3

conn = sqlite3.connect("coins.db")

# conn = sqlite3.connect("new_coins.db")


c = conn.cursor()

c.execute(""" CREATE TABLE wallet (
    id text PRIMARY KEY,
    address text,
    unix_time integer,
    amount integer,
    bnb_price integer,
    timestamp DATE DEFAULT (datetime('now','localtime'))
) """)


# c.execute(""" CREATE TABLE new_coins (
#     id text PRIMARY KEY,
#     symbol text,
#     current_price integer,
#     market_cap integer,
#     address text,
#     unix_time integer,
#     timestamp DATE DEFAULT (datetime('now','localtime'))
# ) """)


conn.commit()

conn.close()
