from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pickle
from PIL import Image
import io
import numpy as np
from sql_users_connection import save_prediction, update_prediction, get_user_predictions
import base64
from google.cloud import storage
import os

app = FastAPI()

GCS_BUCKET_NAME=os.getenv("GCS_BUCKET_NAME")

def load_model_from_gcs(bucket_name, model_filename):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(model_filename)
    model_local_path = f"../models/{model_filename}"
    blob.download_to_filename(model_local_path)
    with open(model_local_path, "rb") as model_file:
        model = pickle.load(model_file)
    return model

model = load_model_from_gcs(GCS_BUCKET_NAME, "cnn_model.pkl")

# Define class labels
class_labels = ['covid', 'lung_opacity', 'normal', 'pneumonia', 'trash']

@app.get("/")
def read_root():
    return {"message": "Welcome to PulmoScanAI"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize((150, 150))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)
        prediction = model.predict(image)

        # Get the highest probability class
        class_idx = np.argmax(prediction[0])
        predicted_label = class_labels[class_idx]

        # If the highest probability is below a threshold, classify as 'trash'
        if prediction[0][class_idx] < 0.5:
            predicted_label = 'trash'

        return JSONResponse(content={"prediction": predicted_label})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
class Prediction(BaseModel):
    user_id: int
    image_data: str  # This will be a base64 encoded string
    original_prediction: str

class UpdatePrediction(BaseModel):
    user_id: int
    image_data: str  # This will be a base64 encoded string
    final_prediction: str
    modified: bool

@app.post("/save_prediction/")
def save_prediction_endpoint(prediction: Prediction):
    try:
        image_data = base64.b64decode(prediction.image_data)  # Decode base64 to bytes
        save_prediction(
            prediction.user_id,
            image_data,
            prediction.original_prediction
        )
        return {"message": "Prediction saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update_prediction/")
def update_prediction_endpoint(prediction: UpdatePrediction):
    try:
        image_data = base64.b64decode(prediction.image_data)  # Decode base64 to bytes
        update_prediction(
            prediction.user_id,
            image_data,
            prediction.final_prediction,
            prediction.modified
        )
        return {"message": "Prediction updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user_predictions/{user_id}")
def user_predictions_endpoint(user_id: int):
    try:
        predictions = get_user_predictions(user_id)
        for prediction in predictions:
            prediction['image_data'] = base64.b64encode(prediction['image_data']).decode('utf-8')  # Encode bytes to base64
        return predictions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))