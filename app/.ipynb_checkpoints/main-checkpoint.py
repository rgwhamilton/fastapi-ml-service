
from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI, HTTPException
from app.schemas import *
model=None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model=joblib.load("models/sentiment_model.joblib")
    yield

app = FastAPI(
    title="Sentiment API",
    lifespan=lifespan
)

@app.get("/")
def home():
    return {"message": "Sentiment API"}

@app.post("/predict",    response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="model not loaded"
        )

    if request.text.strip()=="":
        raise HTTPException(
            status_code=400,
            detail="Input text cannot be empty"
        )

    pred=model.predict([request.text])[0]
    conf=model.predict_proba([request.text]).max()
    label="Positive" if pred==1 else "Negative"

    return PredictionResponse(
        prediction=label, 
        confidence=float(conf)
    )

@app.post("/batch")
def batch(request:BatchPredictRequest):
    if model is None:
        raise HTTPException(
            status_code=503, 
            detail="model not loaded"
        )
    results=[]
    for text in request.texts:
        pred=model.predict([text])[0]
        conf=model.predict_proba([text]).max()
        label="Positive" if pred==1 else "Negative"

        results.append({
            "text":text,
            "prediction":label,
            "confidence":float(conf)
        })
    return {"predictions":results}
