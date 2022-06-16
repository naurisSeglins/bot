import sqlite3

conn = sqlite3.connect("coins.db")

# conn = sqlite3.connect("new_coins.db")


c = conn.cursor()

# c.execute(""" CREATE TABLE bought_trx_approve (
#     hash text
# ) """)


# sql_query = ("ALTER TABLE wallet RENAME TO old_wallet")
# c.execute(sql_query)

sql_query = ("ALTER TABLE wallet ADD last_percent_busd int")
c.execute(sql_query)

# sql_query = ("ALTER TABLE wallet RENAME COLUMN percent TO percent_busd")
# c.execute(sql_query)

# sql_query = ("INSERT INTO wallet(id, address, unix_time) SELECT id, address, unix_time FROM old_wallet")
# c.execute(sql_query)

# c.execute(""" CREATE TABLE wallet (
#     id text PRIMARY KEY,
#     address text,
#     unix_time int,
#     timestamp DATE DEFAULT (datetime('now','localtime')),
#     amount int,
#     first_price_bnb int,
#     bnb_price int,
#     percent_bnb int,
#     percent_busd int,
#     first_price_busd int,
#     busd_price int
# ) """)


conn.commit()

conn.close()
