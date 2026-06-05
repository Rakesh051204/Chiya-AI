import streamlit as st

st.set_page_config(page_title="Chiya AI")

st.title("🌱 Chiya AI SaaS Platform")
st.subheader("Startup-Ready Smart Food Intelligence System")

food = st.text_input("Food Name")
qty = st.number_input("Quantity", min_value=1, value=1)

if st.button("Add Food"):
    st.success(f"{food} added successfully!")

st.header("📊 Dashboard")

st.metric("Total Items", 0)
st.metric("Expired", 0)
st.metric("High Risk", 0)

st.header("🤖 AI Recommendation")
st.info("Supabase integration coming next.")

st.header("📦 Inventory")
st.write("No food items yet.")
