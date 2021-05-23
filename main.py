from typing import Optional
from pymongo import MongoClient
from fastapi import FastAPI
from database import mongo_methods

app = FastAPI()


@app.get("/")
def read_root():
    try:
        return mongo_methods.read()
    except:
        print("An exception occurred")

#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


@app.get("/items")
def read_links(item_id: str):
    return {"link": mongo_methods.read()}


if __name__ == '__main__':
    mg = mongo_methods.MongoAcess()
    print(type(mg.read()))
