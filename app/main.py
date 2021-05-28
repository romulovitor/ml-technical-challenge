from fastapi import FastAPI, Response
from database import mongo_methods
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List
from pydantic import BaseModel
from ml_model.random_forest import get_prediction
from scraping import get_request, parse_request_wrap

app = FastAPI()


class Item(BaseModel):
    name: str
    address: str


@app.get("/it", response_model=List[Item])
async def read_roott():
    mg = mongo_methods.MongoAcess()
    print(mg.string_conection)

    try:

        json_compatible_item_data = jsonable_encoder(mg.read())
        return JSONResponse(content=json_compatible_item_data)
    except:
        print("An exception occurred")


@app.get("/")
def read_root():
    mg = mongo_methods.MongoAcess()
    app_json = mg.read()
    return Response(content=app_json)


# http://127.0.0.1/items/5?q=somequery
@app.get("/items")
def read_links():
    mg = mongo_methods.MongoAcess()
    json_compatible_item_data = jsonable_encoder(mg.insert_mongo())
    return JSONResponse(content=json_compatible_item_data)


@app.get("/prediction/")
def prediction(link: str):
    # http://0.0.0.0/prediction/?link=https://en.wikipedia.org/wiki/Algorithm
    # /items/?link=
    # consulte in db to see if already made the prediction
    # Make it and storage in db
    #link = 'https://en.wikipedia.org/wiki/Algorithm'
    prediction = get_prediction(link)
    print(prediction)

    #json_compatible_item_data = jsonable_encoder(result_from_db)
    json_compatible_item_data = jsonable_encoder({"link": link, "prediction": prediction[0]})
    return JSONResponse(content=json_compatible_item_data)
