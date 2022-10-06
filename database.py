import sqlite3

conn = sqlite3.connect("coins.db")

# conn = sqlite3.connect("new_coins.db")


c = conn.cursor()

# c.execute(""" CREATE TABLE amount_conversion (
#     id text,
#     original int,
#     converted int,
#     timestamp DATE DEFAULT (datetime('now','localtime'))
# ) """)


# sql_query = ("ALTER TABLE new_wallet RENAME TO wallet")
# c.execute(sql_query)


sql_query = ("ALTER TABLE sell_coins ADD error_count int DEFAULT 0")
c.execute(sql_query)


# sql_query = ("INSERT INTO new_wallet(id, address, unix_time, timestamp, amount, first_price_bnb, bnb_price, percent_bnb, highest_percent_bnb, last_percent_bnb) SELECT id, address, unix_time, timestamp, amount, first_price_bnb, bnb_price, percent_bnb, high_percent_bnb, last_percent_bnb FROM wallet;")
# c.execute(sql_query)


# sql_query = ("INSERT INTO wallet(id, address, unix_time) SELECT id, address, unix_time FROM buy_coins")
# c.execute(sql_query)

# c.execute(""" CREATE TABLE sell_coins (
#     id text PRIMARY KEY,
#     address text,
#     unix_time int,
#     timestamp DATE DEFAULT (datetime('now','localtime')),
#     error_count int DEFAULT 0
# ) """)

# c.execute("ALTER TABLE new_coins RENAME COLUMN highest_percent_bnb TO first_percent_bnb")

# c.execute(""" CREATE TABLE sell_calculation_history (
#     id text PRIMARY KEY,
#     address text,
#     unix_time int,
#     timestamp DATE DEFAULT (datetime('now','localtime')),
#     amount int,
#     first_price_bnb int,
#     bnb_price int,
#     percent_bnb int,
#     highest_percent_bnb int,
#     last_percent_bnb int
# ) """)


conn.commit()

conn.close()
