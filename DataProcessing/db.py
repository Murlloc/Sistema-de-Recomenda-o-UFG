import pymongo

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.StoreDB
    mongo.server_info()
except:
    print("deu ruim")

def getReviewsOnBooks(paginadorInicio, paginadorFim):
    return db.cleanBooksReviews2.find(
            {
                "_id": {
                    "$gt":paginadorInicio, 
                    "$lte": paginadorFim
                    }
            },{
                "timestamp":0, 
                "_id":0
            })