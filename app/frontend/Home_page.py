import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to PulmoScanAI ! 👋")

st.page_link("Home_page.py", label="Home", icon="🏠")
st.page_link("pages/Prediction_page.py", label="Prediction Page", icon="1️⃣")