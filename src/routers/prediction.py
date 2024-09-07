# src/routers/prediction.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.models.ml_model import predict

router = APIRouter()

class PredictionRequest(BaseModel):
    input_data: str

@router.post("/predict/")
async def make_prediction(request: PredictionRequest):
    prediction = predict(request.input_data)
    return {"prediction": prediction}
