import sqlite3

conn = sqlite3.connect("market.db")
c = conn.cursor()

# PRODUCTS TABLOSU
c.execute("""
CREATE TABLE IF NOT EXISTS products (
    barcode TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    stock INTEGER
)
""")

# RETURNS TABLOSU
c.execute("""
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    quantity INTEGER,
    total_price REAL,
    date TEXT
)
""")

conn.commit()
conn.close()

print("DB hazır")
