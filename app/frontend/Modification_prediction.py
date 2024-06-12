import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Modification page")
st.markdown("# Modification Page")

if st.button('Normal'):
    print("Normal")
elif st.button('Pneumonia'):
    print("Pneumonia")
elif st.button('Covid'):
    print("Covid")
elif st.button('Lung_opacity'):
    print("Lung_opacity")
