# DATABASE LAYER
conn = sqlite3.connect("food.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS food (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity INTEGER,
    expiry TEXT
)
""")

conn.commit()
