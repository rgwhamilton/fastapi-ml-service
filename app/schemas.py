
from typing import List
from pydantic import BaseModel

class PredictionRequest(BaseModel):
    text:str

class PredictionResponse(BaseModel):
    prediction:str
    confidence:float

class BatchPredictionRequest(BaseModel):
    texts:List[str]
