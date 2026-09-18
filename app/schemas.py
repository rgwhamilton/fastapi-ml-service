
from typing import List
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    text: str = Field(
        ..., 
        min_length=5, 
        max_length=1000,
        description="Input text for sentiment analysis", 
        examples=["This movie was absolutely fantastic!"
        ]
    )

class PredictionResponse(BaseModel):
    prediction:str
    confidence:float

class BatchPredictionRequest(BaseModel):
    texts:List[str]
