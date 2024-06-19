import streamlit as st
import requests
from PIL import Image
import io
import base64

def show():
    st.markdown("# Prediction Page")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        buf = io.BytesIO()
        image.save(buf, format='PNG' if uploaded_file.type == 'image/png' else 'JPEG')
        byte_im = buf.getvalue()
        image_data = base64.b64encode(byte_im).decode('utf-8')
        
        if st.button('Predict'):
            files = {"file": (uploaded_file.name, byte_im, uploaded_file.type)}
            response = requests.post("http://127.0.0.1:8000/predict/", files=files)
            if response.status_code == 200:
                st.write('Prediction:', response.json()['prediction'])
            else:
                st.write('Error:', response.status_code, response.json()['detail'])
        
        if st.button('Modify'):
            st.session_state['image_data'] = image_data
            st.session_state['page'] = 'Update_prediction'
            st.experimental_rerun()
