from fastapi import APIRouter, status
from app.api.pydantic_models import Flower, FlowerFeatures, InferenceModel, CLASS_MAPPING, PredictionHistory
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
from app.api.routers.report import prediction_history
from datetime import datetime
router = APIRouter()

# create a way to store features and predictions (in a list)
def log_prediction_history(prediction_results: Flower):
    prediction_history.append(PredictionHistory(
        prediction=prediction_results, execution_time=datetime.now()))


@router.post("predict", status_code=status.HTTP_200_OK, response_model=Flower)
def predict_specie(measurements: FlowerFeatures, model_name: InferenceModel = InferenceModel.DEFAULT_MODEL):
    with open(f"app/models/serialized/{model_name}.pickle", "rb") as serialized_model:
        model: RandomForestClassifier = pickle.load(serialized_model)

    feat = np.array([v for k, v in measurements.dict().items()])
    model_input = feat.reshape(1, -1)
    prediction_result = model.predict(X=model_input)

    results = Flower(specie=CLASS_MAPPING.get(
        prediction_result[0]), measurements=measurements)
    log_prediction_history(prediction_results=results)
    return results
