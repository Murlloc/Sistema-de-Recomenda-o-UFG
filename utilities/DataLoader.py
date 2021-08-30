import pymongo
import json

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
    count = 3
    id = 500001
    while count < 30:
        if count == 29:
            with open('./DataSet/ratings_Books_Ultima.json') as f:
                file_data = json.load(f)
        else:
            with open('./DataSet/ratings_Books_'+str(count)+'.json') as f:
                file_data = json.load(f)
        count = count + 1
        try:
            aux = 0
            for documento in file_data:
                documento['_id'] = id
                db.cleanBooksReviews2.insert_one(documento)
                print(str(aux))
                aux = aux + 1
                id = id + 1
        except:
            print("Error on insert")
    with open('./DataSet/ratings_Books_1' + '.json') as f:
            file_data = json.load(f)
    aux = 0
    for documento in file_data:
            documento['_id'] = id
            db.cleanBooksReviews2.insert_one(documento)
            print(str(aux))
            aux = aux + 1
            id = id + 1
except:
    print("Error on the json file")
