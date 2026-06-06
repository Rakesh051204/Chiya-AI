import streamlit as st
import pandas as pd
from datetime import date
from supabase import create_client

# =========================
# SUPABASE CONFIG
# =========================

SUPABASE_URL = "https://grgefavcsqpmdicuvfvy.supabase.co"
SUPABASE_KEY = "sb_publishable_XWDVocxI3J1wrdAHKLKsEA_6bYZv-gV"

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
# ADD FOOD
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
    value=date.today()
)

if st.button("Add Food"):

    if food.strip() == "":
        st.warning("Please enter food name")

    else:

        try:

            supabase.table("food_items").insert({
                "food_name": food,
                "quantity": int(qty),
                "expiry_date": str(expiry_date)
            }).execute()

            st.success(f"✅ {food} added successfully!")

        except Exception as e:
            st.error(f"Error: {e}")

# =========================
# LOAD DATA
# =========================

foods = []

try:

    response = (
        supabase
        .table("food_items")
        .select("*")
        .execute()
    )

    foods = response.data

except Exception as e:

    st.error(f"Database Error: {e}")

# =========================
# DASHBOARD
# =========================

today = date.today()

total_items = len(foods)
expired = 0
high_risk = 0

for item in foods:

    exp_date = pd.to_datetime(
        item["expiry_date"]
    ).date()

    if exp_date < today:
        expired += 1

    days_left = (exp_date - today).days

    if 0 <= days_left <= 3:
        high_risk += 1

st.header("📊 Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("Total Items", total_items)
c2.metric("Expired", expired)
c3.metric("High Risk", high_risk)

# =========================
# AI RECOMMENDATION
# =========================

st.header("🤖 AI Recommendation")

alerts = []

for item in foods:

    exp_date = pd.to_datetime(
        item["expiry_date"]
    ).date()

    days_left = (exp_date - today).days

    if 0 <= days_left <= 3:

        alerts.append(
            f"⚠️ Use {item['food_name']} soon ({days_left} day(s) left)"
        )

if alerts:

    for alert in alerts:
        st.warning(alert)

else:

    st.success(
        "🎉 No foods are close to expiry."
    )

# =========================
# INVENTORY
# =========================

st.header("📦 Inventory")

if len(foods) > 0:

    rows = []

    for item in foods:

        exp_date = pd.to_datetime(
            item["expiry_date"]
        ).date()

        days_left = (
            exp_date - today
        ).days

        if days_left < 0:
            status = "Expired"
        elif days_left <= 3:
            status = "High Risk"
        else:
            status = "Fresh"

        rows.append({
            "Food": item["food_name"],
            "Quantity": item["quantity"],
            "Expiry Date": item["expiry_date"],
            "Days Left": days_left,
            "Status": status
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df,
        use_container_width=True
    )

else:

    st.info("No food items yet.")
