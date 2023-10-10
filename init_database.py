import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

cur.execute("CREATE TABLE prices(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "symbol text, price float, extraction_time timestamp)")