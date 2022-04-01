import sqlite3

conn = sqlite3.connect("coins.db")

# conn = sqlite3.connect("new_coins.db")


c = conn.cursor()

c.execute(""" CREATE TABLE coin_watcher (
    unix_time int
) """)


# c.execute(""" CREATE TABLE coins_on_scanner (
#     id text PRIMARY KEY,
#     symbol text,
#     address text,
#     unix_time integer,
#     timestamp DATE DEFAULT (datetime('now','localtime'))
# ) """)


conn.commit()

conn.close()
