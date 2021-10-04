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

def getUser(userID):
    result = db.BooksPredictions.find({
        "rawID" : userID
        }, {
            "_id": 0, "rawID" : 1
            }).count()
    if result == 0:
        return False
    else:
        return True

def insertBookPrediction(prediction):
    try:
        db.BooksPredictions.insert(prediction)
        return True
    except Exception:
        return False

def getReviewsOnBooks(paginadorInicio, paginadorFim):
    return db.booksReviews.find(
            {},{
                "_id":0,
                "reviewerID": 1,
                "asin": 1,
                "overall": 1
            }).skip(paginadorInicio).limit(paginadorFim)

def getBooksPredictions(userID):
    result = db.BooksPredictions.find({
        "rawID" : userID
        }, {
            "_id": 0
            })
    return result

def getBook(bookID):
    result = db.books.find_one({
        "asin" : bookID
        }, {
            "_id": 0,
            "asin": 1,
            "title": 1,
            "price": 1,
            "description": 1,
            "imUrl": 1
            })
    return result