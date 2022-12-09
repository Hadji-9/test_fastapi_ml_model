from typing import List
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.api.pydantic_models import PredictionHistory
from app.models.model import distribution_plots
from datetime import datetime
router = APIRouter()
prediction_history: List[PredictionHistory] = []


@router.get("/history", status_code=status.HTTP_200_OK, response_model=List[PredictionHistory])
def get_history(from_this_time: datetime = None):
    if from_this_time:
        preds = [pred for pred in prediction_history if pred.time > from_this_time]
    else:
        preds = prediction_history
    return preds
# create a function to plot training data distribution and stored data distribution


@router.get("/distribution", status_code=status.HTTP_200_OK)
def get_history(history: bool = False):
    if history:

        plot = distribution_plots(data=prediction_history)
    else:
        plot = distribution_plots()
    return JSONResponse(content=plot)
