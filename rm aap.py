import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.set_page_config(page_title="Chiya AI SaaS", layout="wide")
st.title("🌱 Chiya AI SaaS Platform (Phase 4)")
st.subheader("Startup-Ready Smart Food Intelligence System")

conn = sqlite3.connect("food.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS food (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT,
        quantity INTEGER,
        expiry   TEXT
    )
""")
conn.commit()

def add_food(name, qty, expiry):
    c.execute("INSERT INTO food (name, quantity, expiry) VALUES (?, ?, ?)", (name, qty, expiry))
    conn.commit()

def delete_food(food_id):
    c.execute("DELETE FROM food WHERE id=?", (food_id,))
    conn.commit()

def load_food():
    return pd.read_sql("SELECT * FROM food", conn)

def ai_score(food, days_left):
    food = food.lower()
    if food in ["milk", "curd", "chicken", "fish", "biriyani"]:
        base = 7
    elif food in ["rice", "vegetables", "apple"]:
        base = 5
    else:
        base = 3
    urgency = max(0, 10 - days_left)
    return base + urgency

df = load_food()
if len(df) > 0:
    df["expiry"] = pd.to_datetime(df["expiry"]).dt.date
    today = date.today()
    df["days_left"] = df["expiry"].apply(lambda x: (x - today).days)
    df["ai_score"] = df.apply(lambda row: ai_score(row["name"], row["days_left"]), axis=1)

st.header("➕ Add Food")
name   = st.text_input("Food Name")
qty    = st.number_input("Quantity", min_value=1, value=1)
expiry = st.date_input("Expiry Date")
if st.button("Add Food"):
    if name:
        add_food(name, qty, expiry)
        st.success("Added!")
        st.rerun()

st.header("📊 AI Dashboard")
if len(df) > 0:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Items", len(df))
    col2.metric("Expired",     len(df[df["days_left"] < 0]))
    col3.metric("High Risk",   len(df[df["ai_score"] > 10]))

st.header("🤖 What Should I Eat?")
if len(df) > 0:
    urgent = df[df["ai_score"] > 12].sort_values("ai_score", ascending=False)
    medium = df[(df["ai_score"] > 7) & (df["ai_score"] <= 12)]
    if len(urgent) > 0:
        st.error("🔥 EAT THESE NOW")
        for _, row in urgent.iterrows():
            st.write(f"- {row['name']} (AI Score {row['ai_score']})")
    elif len(medium) > 0:
        st.warning("🟡 Eat Soon")
        for _, row in medium.iterrows():
            st.write(f"- {row['name']}")
    else:
        st.success("🟢 Everything is safe")

st.header("📦 AI Ranked Inventory")
if len(df) > 0:
    df = df.sort_values("ai_score", ascending=False)
    for _, row in df.iterrows():
        if row["days_left"] < 0:
            st.error(f"🔴 {row['name']} EXPIRED")
        elif row["ai_score"] > 12:
            st.error(f"🔥 {row['name']} CRITICAL")
        elif row["ai_score"] > 7:
            st.warning(f"🟡 {row['name']} MEDIUM")
        else:
            st.success(f"🟢 {row['name']} SAFE")
        if st.button(f"🗑️ Delete {row['id']}", key=row["id"]):
            delete_food(row["id"])
            st.rerun()
