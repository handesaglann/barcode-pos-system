import sqlite3

conn = sqlite3.connect("market.db")
c = conn.cursor()

# Günlük satış özeti tablosu
c.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    total REAL
)
""")

# Satış detayları (ürün bazlı)
c.execute("""
CREATE TABLE IF NOT EXISTS sale_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_date TEXT,
    barcode TEXT,
    product_name TEXT,
    price REAL
)
""")

conn.commit()
conn.close()

print("sales ve sale_items tabloları hazır")
