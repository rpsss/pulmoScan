from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pickle
from PIL import Image
import io
import numpy as np

app = FastAPI()

# Load the model
with open('../../models/cnn_model.pkl', 'rb') as f:
    model = pickle.load(f)

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