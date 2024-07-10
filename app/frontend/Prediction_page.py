import streamlit as st
from PIL import Image
import requests
import io
import base64

def show():
    st.markdown("# Prédiction")
    
    uploaded_file = st.file_uploader("Importez votre image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Image téléchargée', use_column_width=True)
        
        buf = io.BytesIO()
        image.save(buf, format='PNG' if uploaded_file.type == 'image/png' else 'JPEG')
        byte_im = buf.getvalue()  # Get image bytes
        image_data = base64.b64encode(byte_im).decode('utf-8')  # Encode image bytes to base64
        
        if st.button('Prédire'):
            files = {"file": (uploaded_file.name, byte_im, uploaded_file.type)}
            response = requests.post("http://127.0.0.1:8000/predict/", files=files)
            if response.status_code == 200:
                prediction = response.json()['prediction']
                st.write('Prediction:', prediction)
                
                # Save prediction to database
                user_id = st.session_state.get('user_id')
                save_prediction(user_id, byte_im, prediction)
            else:
                st.write('Error:', response.status_code, response.json()['detail'])
        
        if st.button('Modification'):
            st.session_state['image_data'] = image_data
            st.session_state['page'] = 'Update_prediction'
            st.experimental_rerun()

def save_prediction(user_id, image_data, original_prediction):
    response = requests.post(
        "http://127.0.0.1:8000/save_prediction/",
        json={"user_id": user_id, "image_data": base64.b64encode(image_data).decode('utf-8'), "original_prediction": original_prediction}
    )
    if response.status_code != 200:
        st.error("Impossible de sauvegarder la prédiction. Veuillez réessayer.")
