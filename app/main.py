import time
import logging
from contextlib import asynccontextmanager
import joblib
from fastapi import FastAPI, HTTPException, Request
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

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start=time.time()
    response=await call_next(request)
    duration=time.time()-start
    response.headers["X-Process-Time"]=str(round(duration,4))
    logging.info(
        f"{request.method} {request.url.path} {response.status_code} {duration:.4f}s"
    )
    return response

@app.get("/")
def home():
    return {"message": "Sentiment API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
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
def batch(request:BatchPredictionRequest):
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
