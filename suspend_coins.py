import sqlite3

def suspending_coins():

    conn = sqlite3.connect("coins.db")

    c = conn.cursor()

    c.execute("SELECT address, error_count FROM sell_coins")
    coin_data = c.fetchall()

    for data in coin_data:
            if data[1] == 3:
                c.execute("INSERT INTO suspended_coins(id, address, error_count) SELECT id, address, error_count FROM sell_coins WHERE address > :address",{'address': data[0]})

    conn.commit()

    c.execute("SELECT address, error_count FROM buy_coins")
    coin_data = c.fetchall()

    for data in coin_data:
            if data[1] == 3:
                c.execute("INSERT INTO suspended_coins(id, address, error_count) SELECT id, address, error_count FROM buy_coins WHERE address > :address",{'address': data[0]})

    conn.commit()

    c.execute("SELECT address FROM suspended_coins")
    coin_data = c.fetchall()

    for data in coin_data:
        c.execute("DELETE FROM buy_coins WHERE address = ?", (data[0],))
        c.execute("DELETE FROM sell_coins WHERE address = ?", (data[0],))

    conn.commit()

    conn.close()