from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import pickle
from PIL import Image
import io
import numpy as np

app = FastAPI()

# Charger le modèle
with open('../../notebook/cnn_model.pkl', 'rb') as f:
    model = pickle.load(f)

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
        return JSONResponse(content={"prediction": int(np.argmax(prediction[0]))})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
