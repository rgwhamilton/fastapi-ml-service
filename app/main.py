

from fastapi import FastAPI

app = FastAPI(title="Production Sentiment API")

@app.get("/")
def home():
    return {"message":"Docker Compose Demo"}

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.get("/metrics")
def metrics():
    return {
        "requests":120, 
        "latency_ms":42
    }

