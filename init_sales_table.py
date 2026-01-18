import sqlite3

conn = sqlite3.connect("market.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    total REAL
)
""")

conn.commit()
conn.close()

print("sales tablosu hazır")
