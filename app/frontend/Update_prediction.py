import streamlit as st
from PIL import Image
import io
import base64
from backend.sql_users_connection import save_image_to_db

def show(image_data):
    st.markdown("# Update Prediction")

    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    def save_and_redirect(label):
        save_image_to_db(base64.b64decode(image_data), label)
        st.success(f"Saved as {label.capitalize()}")
        st.session_state['page'] = 'Home'
        st.experimental_rerun()

    if st.button('COVID'):
        save_and_redirect('covid')
    if st.button('Normal'):
        save_and_redirect('normal')
    if st.button('Pneumonia'):
        save_and_redirect('pneumonia')
    if st.button('Lung Opacity'):
        save_and_redirect('lung_opacity')
