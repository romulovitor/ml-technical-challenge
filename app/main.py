from typing import Optional
from pymongo import MongoClient
from fastapi import FastAPI, Response
from database import mongo_methods
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json

from typing import List
from pydantic import BaseModel
from database.mongo_methods import MongoAcess

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
    print(mg.insert_mongo())
    print(type(mg.read()))
    json_compatible_item_data = jsonable_encoder(mg.insert_mongo())
    return JSONResponse(content=json_compatible_item_data)
