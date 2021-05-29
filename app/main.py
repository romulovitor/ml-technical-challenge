from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ml_model.random_forest import get_prediction

app = FastAPI()


@app.get("/")
def read_root():
    return {"Meli": "Welcome to my teste"}


@app.get("/prediction/")
def prediction(link: str):
    """
    Endpoint to receive and provide the prediction
    :param link: The url inform by user
    :return: Prediction to user
    """
    prediction = get_prediction(link)
    json_compatible_item_data = jsonable_encoder({"link": link, "prediction": prediction})
    return JSONResponse(content=json_compatible_item_data)
