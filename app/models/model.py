# this file will contain code related to your model
# training (or loading of a pre-trained model)
# prediction
# reporting, possibly


from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from typing import Tuple
from sklearn import datasets
import pickle
from app.api.pydantic_models import InferenceModel
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.embed import json_item
iris = datasets.load_iris()


def load_data(custom_data: Tuple[list] = None):
    if custom_data:
        df = pd.DataFrame(custom_data, columns=iris.feature_names)
    else:
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
    return df


def train_model(data_frame: pd.DataFrame, model_alias: str = InferenceModel.DEFAULT_MODEL):

    data_frame['species'] = np.array(
        [iris.target_names[i] for i in iris.target])
    X_train, X_test, y_train, y_test = train_test_split(
        data_frame[iris.feature_names], iris.target, test_size=0.5, stratify=iris.target, random_state=123456)

    model = RandomForestClassifier(
        n_estimators=100, oob_score=True, random_state=123456)
    model.fit(X_train, y_train)
    predicted = model.predict(X_test)
    accuracy = accuracy_score(y_test, predicted)
    print(f'Out-of-bag score estimate: {model.oob_score_:.3}')
    print(f'Mean accuracy score: {accuracy:.3}')
    return model_alias, model


def serialize_model(model_alias: str, model_to_serialized):
    with open(f"app/models/serialized/{model_alias}.pickle", "wb") as serialized_model:
        pickle.dump(model_to_serialized, serialized_model)


def make_plot(title, hist, edges, x):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5)

    return p


def distribution_plots(data: BaseModel):
    x = np.linspace(-2, 2, 1000)
    plots = []
    if data:
        df = pd.DataFrame(jsonable_encoder(data))
    else:
        df = pd.DataFrame(iris.data, columns=iris.feature_names)
    for feature in iris.feature_names:
        data = df[feature]
        hist, edges = np.histogram(data, density=True, bins=10)
        plot = make_plot(f"distribution for {feature}", hist, edges, x)
        plots.append(plot)
    return json_item(gridplot(plots, ncols=2, width=400, height=400, toolbar_location=None))
