import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Chiya AI SaaS", layout="wide")

# -------------------------
# DATABASE
# -------------------------
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

# -------------------------
# FUNCTIONS
# -------------------------
def add_food(name, qty, expiry):
    c.execute(
        "INSERT INTO food (name, quantity, expiry) VALUES (?, ?, ?)",
        (name, qty, str(expiry))
    )
    conn.commit()

def delete_food(food_id):
    c.execute("DELETE FROM food WHERE id=?", (food_id,))
    conn.commit()

def load_food():
    return pd.read_sql_query("SELECT * FROM food", conn)
