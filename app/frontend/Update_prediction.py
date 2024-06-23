import streamlit as st
from PIL import Image
import requests
import io
import base64

def show():
    st.markdown("# Update Prediction")

    image_data = st.session_state['image_data']
    user_id = st.session_state.get('user_id')
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    def save_and_redirect(label):
        update_prediction(user_id, base64.b64decode(image_data), label)
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

def update_prediction(user_id, image_data, final_prediction):
    response = requests.post(
        "http://127.0.0.1:8000/update_prediction/",
        json={"user_id": user_id, "image_data": base64.b64encode(image_data).decode('utf-8'), "final_prediction": final_prediction, "modified": True}
    )
    if response.status_code != 200:
        st.error("Failed to update prediction")
