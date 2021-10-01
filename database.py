import sqlite3

conn = sqlite3.connect("coins.db")

c = conn.cursor()

c.execute(""" CREATE TABLE coins (
    id text PRIMARY KEY,
    symbol text,
    current_price integer,
    market_cap integer,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
) """)

# c.execute(""" CREATE TABLE coins (
#     id text PRIMARY KEY,
#     symbol text,
#     current_price integer,
#     market_cap integer
# ) """)

# c.execute("INSERT INTO employees VALUES ('Nauris', 'Seglins', 100)")

# c.execute("SELECT * FROM employees WHERE last='Seglins'")

# print(c.fetchall())

conn.commit()

conn.close()
