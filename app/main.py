
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.prediction import router
from configs.settings import APP_NAME, API_VERSION

app = FastAPI(
    title = APP_NAME, 
    version = API_VERSION, 
    description = "Production Ready Sentiment Analysis API"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"],
)

app.include_router(router)
@app.get(
    "/",
    summary = "Home", 
    tags = ["General"]
)
def home():
    return {
        "message": "Welcome to Sentiment API"
    }
