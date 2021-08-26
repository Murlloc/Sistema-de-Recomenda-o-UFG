from flask import Flask
import pymongo
app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017
    )
    db = mongo.company
    mongo.server_info()
except:
    print("deu ruim")

#################### Routes ################################

@app.route("/", methods=["GET"])
def HelloWorld():
    return {"Hello World": 123}

@app.route("/userCreate", methods=["POST"])
def createUser():
    user = {
        "name": "A",
        "idade": 19
    }
    dbResponse = db.users.insert_one(user)
    print(dbResponse.inserted_id)
    return str(dbResponse.inserted_id)

###########################################################

if __name__ == "__main__":
    app.run(port=8080, debug=True)