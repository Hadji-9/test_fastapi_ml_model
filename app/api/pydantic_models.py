
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class Specie(str, Enum):
    SETOSA = "SETOSA"
    VIRGINICA = "VIRGINICA"
    VERSICOLOR = "VERSICOLOR"


CLASS_MAPPING = {
    0: Specie.SETOSA,
    1: Specie.VERSICOLOR,
    2: Specie.VIRGINICA
}


class InferenceModel(str, Enum):
    DEFAULT_MODEL = "DEFAULT_MODEL"
    LOGISTIC_REG = "LOGISTIC_REG"
    SVM = "SVM"


class FlowerFeatures(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)


class Flower(BaseModel):
    measurements: FlowerFeatures
    specie: Specie


class PredictionHistory(BaseModel):
    prediction: Flower
    execution_time: datetime
