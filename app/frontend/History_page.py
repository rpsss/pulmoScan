import streamlit as st
import requests
from PIL import Image
import io
import base64

def show():
    st.markdown("# My Predictions")
    
    user_id = st.session_state.get('user_id')
    response = requests.get(f"http://127.0.0.1:8000/user_predictions/{user_id}")
    
    if response.status_code == 200:
        predictions = response.json()
        for prediction in predictions:
            st.write(f"Original Prediction: {prediction['original_prediction']}")
            if prediction['modified']:
                st.write(f"Final Prediction: {prediction['final_prediction']}")
            else:
                st.write("Final Prediction: Not modified")
                
            image_data = base64.b64decode(prediction['image_data'])
            image = Image.open(io.BytesIO(image_data))
            st.image(image, caption='Predicted Image', use_column_width=True)
            st.write("---")
    else:
        st.error("Failed to fetch predictions")
