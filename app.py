import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client

# =========================
# SUPABASE CONFIG
# =========================
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# =========================
# SUPABASE CONFIG
# =========================
SUPABASE_URL = "https://abcdefghijk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Chiya AI",
    page_icon="🌱",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("🌱 Chiya AI SaaS Platform")
st.subheader("Startup-Ready Smart Food Intelligence System")

# =========================
# ADD FOOD FORM
# =========================
st.header("➕ Add Food")

food = st.text_input("Food Name")

qty = st.number_input(
    "Quantity",
    min_value=1,
    value=1
)

expiry_date = st.date_input(
    "Expiry Date",
    min_value=date.today()
)

if st.button("Add Food"):
    if food.strip() == "":
        st.warning("Please enter food name")
    else:
        supabase.table("food_items").insert({
            "food_name": food,
            "quantity": int(qty),
            "expiry_date": str(expiry_date)
        }).execute()

        st.success(f"✅ {food} added successfully!")

# =========================
# FETCH DATA
# =========================
try:
    response = supabase.table("food_items").select("*").execute()
    foods = response.data
except:
    foods = []

# =========================
# DASHBOARD CALCULATIONS
# =========================
today = date.today()

total_items = len(foods)
expired = 0
high_risk = 0

for item in foods:
    exp_date = pd.to_datetime(item["expiry_date"]).date()

    if exp_date < today:
        expired += 1

    days_left = (exp_date - today).days

    if 0 <= days_left <= 3:
        high_risk += 1

# =========================
# DASHBOARD
# =========================
st.header("📊 Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Items", total_items)
col2.metric("Expired", expired)
col3.metric("High Risk", high_risk)

# =========================
# AI RECOMMENDATION
# =========================
st.header("🤖 AI Recommendation")

recommendations = []

for item in foods:
    exp_date = pd.to_datetime(item["expiry_date"]).date()
    days_left = (exp_date - today).days

    if 0 <= days_left <= 3:
        recommendations.append(
            f"⚠️ Use {item['food_name']} soon ({days_left} day(s) left)"
        )

if recommendations:
    for rec in recommendations:
        st.info(rec)
else:
    st.success("🎉 No foods are at risk of expiring.")

# =========================
# INVENTORY
# =========================
st.header("📦 Inventory")

if foods:

    inventory_data = []

    for item in foods:

        exp_date = pd.to_datetime(item["expiry_date"]).date()
        days_left = (exp_date - today).days

        if days_left < 0:
            status = "Expired"
        elif days_left <= 3:
            status = "High Risk"
        else:
            status = "Fresh"

        inventory_data.append({
            "Food": item["food_name"],
            "Quantity": item["quantity"],
            "Expiry Date": item["expiry_date"],
            "Days Left": days_left,
            "Status": status
        })

    df = pd.DataFrame(inventory_data)

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.write("No food items yet.")
