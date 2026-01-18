import sqlite3

conn = sqlite3.connect("market.db")
c = conn.cursor()

c.execute("""
CREATE TABLE products (
    barcode TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    stock INTEGER
)
""")

c.execute("INSERT INTO products VALUES ('111', 'Su', 5.0, 10)")
c.execute("INSERT INTO products VALUES ('222', 'Ekmek', 10.0, 5)")

conn.commit()
conn.close()

print("DB hazır")
