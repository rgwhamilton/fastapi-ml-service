

import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

app = FastAPI(
    title="Production Sentiment API",
    version="1.0"
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
    return {"message":"Production API Running"}

@app.get("/health")
def health():
    return {"status":"healthy"}

