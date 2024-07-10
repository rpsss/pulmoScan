import streamlit as st
import requests
from PIL import Image
import io
import base64

def show():
    st.markdown("# Mes Prédictions")
    
    user_id = st.session_state.get('user_id')
    response = requests.get(f"http://127.0.0.1:8000/user_predictions/{user_id}")
    
    if response.status_code == 200:
        predictions = response.json()
        for prediction in predictions:
            st.write(f"Prédiction de départ : {prediction['original_prediction']}")
            if prediction['modified']:
                st.write(f"Prédiction finale : {prediction['final_prediction']}")
            else:
                st.write(" *Prédiction non modifiée*")
                
            image_data = base64.b64decode(prediction['image_data'])
            image = Image.open(io.BytesIO(image_data))
            st.image(image, caption='Image Prédite', use_column_width=True)
            st.write("---")
    else:
        st.error("Impossible de récupérer vos prédictions. Veuillez réessayer.")
