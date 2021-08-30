import pymongo
import json
import pandas as pd

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.StoreDB
    mongo.server_info()
except:
    print("deu ruim")

try:
    dbResponse = db.cleanBooksReviews.find({},{"timestamp":0}).limit(1000)
    dataFrame = pd.DataFrame(dbResponse)
    print(dataFrame.count())
    print(dataFrame.head())
    #output = [{item: data[item] for item in data if item != '_id'} for data in dbResponse]
except:
    print("Deu ruim na leitura")