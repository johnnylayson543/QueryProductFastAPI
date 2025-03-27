from typing import Union

from fastapi import FastAPI

import json
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.objectid import ObjectId


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/getSingleProduct")
def get_single_product():

    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client.assignment
    collection = db.products

    # ID of the object
    id = '67d2bf4535fbb8f2bf334d3d'
    query = {"_id": ObjectId(id)}
    filter = {"_id": 0}

    # find it
    results = collection.find_one(query, filter)
    print(results)

    # dump to JSON
    results = dumps(results)

    #return
    return json.loads(results)

@app.get("/getAll")
def get_all():
    client = MongoClient("mongodb://root:example@localhost:27017/")
    db = client.assignment
    collection = db.products
    results = dumps(collection.find())

    print(results)
    return json.loads(results)

@app.get("/addNew")
def add_new():
    client = MongoClient("mongodb://root:example@localhost:27017/")

    db = client.assignment

    collection = db.products

    # Record to be inserted
    newRecord = {"Product ID": 'AUTO020', "Name": 'Car Wheels', "Unit Price": 50, "Stock Quantity": 40, "Description": 'A Car Wheel'}
    # newRecord = {"Product ID": 'AUTO020'}

    # insert it
    res = collection.insert_one(newRecord)
    print(newRecord)
    #return
    return {"Add":"New"}

@app.get("/deleteOne")
def delete_one():
    client = MongoClient("mongodb://root:example@localhost:27017/")

    db = client.assignment

    collection = db.products

    deleteRecord = {"Product ID": 'AUTO020'}

    # delete it
    res = collection.delete_one(deleteRecord)

    # Check if deletion was successful
    if res.deleted_count > 0:
        print("Document deleted successfully!")
    else:
        print("No document matched the query.")

    return {"Delete": "One"}

@app.get("/startsWith/{letter}")
def starts_with(letter:str):

    client = MongoClient("mongodb://root:example@localhost:27017/")

    db = client.assignment

    collection = db.products

    queryRecord = {"Product ID": {"$regex": "^A", "$options": "i"}}

    # find it
    res = collection.find(queryRecord)

    print(queryRecord)

    # Print matching documents
    for doc in res:
        print(doc)

    return {"Starts" : "With"}

@app.get("/paginate")
def paginate():

    client = MongoClient("mongodb://root:example@localhost:27017/")

    db = client.assignment

    collection = db.products

    page = 1  # Current page number
    page_size = 5  # Number of documents per page

    # Calculate the number of documents to skip
    skip_count = (page - 1) * page_size

    queryRecord = {"Product ID": {"$regex": "^A", "$options": "i"}}
    res = collection.find(queryRecord).skip(skip_count).limit(page_size)

    # Print paginated results
    for doc in res:
        print(doc)

    # Get total number of documents (for pagination info)
    total_count = collection.count_documents(queryRecord)
    total_pages = -(-total_count // page_size)  # Equivalent to ceil(total_count / page_size)

    print(f"Total Documents: {total_count}")
    print(f"Total Pages: {total_pages}")
    print(f"Current Page: {page}")

    return {"Paginate": "Paginate"}

@app.get("/convert")
def convert():
    return {"Convert": "Convert"}
