from flask import Flask
import pymongo
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.StoreDB
    mongo.server_info()
except:
    print("deu ruim")

#################### Routes ################################

@app.route("/", methods=["GET"])
def HelloWorld():
    return {"Hello World": 123}

# [{"reviewr_id": "FODA-SE", "asin": "123123","overall": 5.0},
# [reviewr_id2,asin2,overall2]...]

@app.route("/users", methods=["GET"])
def getUsers():
    dbResponse = db.cleanBooksReviews.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in dbResponse]
    return output

@app.route("/userCreate", methods=["POST"])
def createUser():
    user = {
        "name": "B",
        "idade": 29
    }
    dbResponse = db.users.insert_one(user)
    print(dbResponse.inserted_id)
    return str(dbResponse.inserted_id)

###########################################################

if __name__ == "__main__":
    app.run(port=8081, debug=True)