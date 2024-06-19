import streamlit as st
from backend.sql_users_connection import get_user_predictions
from PIL import Image
import io
import base64

def show(user_id):
    st.title("Prediction History")

    predictions = get_user_predictions(user_id)

    if not predictions:
        st.write("No predictions found.")
        return

    for prediction in predictions:
        st.markdown("---")
        image_data = prediction['image_data']
        original_prediction = prediction['original_prediction']
        final_prediction = prediction['final_prediction']
        modified = prediction['modified']
        created_at = prediction['created_at']
        modified_at = prediction['modified_at']
        
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption='Predicted Image', use_column_width=True)
        
        st.write(f"**Original Prediction:** {original_prediction}")
        if modified:
            st.write(f"**Final Prediction:** {final_prediction}")
            st.write(f"**Modified At:** {modified_at}")
        else:
            st.write(f"**Prediction:** {final_prediction}")
        st.write(f"**Predicted At:** {created_at}")
