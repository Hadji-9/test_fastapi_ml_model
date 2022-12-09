from fastapi import FastAPI
from app.api.routes import router
from app.models.model import serialize_model, train_model, load_data


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def startup_event():
    print("******* APPLICATION STARTUP *******")
    data = load_data()
    model: tuple = train_model(data_frame=data)
    serialize_model(*model)
