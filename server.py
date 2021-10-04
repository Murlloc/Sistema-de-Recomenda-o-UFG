from flask import Flask, request
import pymongo
import DataProcessing.db as db
app = Flask(__name__)

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

@app.route("/list/<user_id>/<type>", methods=["GET"])
def getPredictions(user_id, type):
    itens = []
    dbResponse = db.getBooksPredictions(user_id)
    for element in dbResponse:
        for item in element['itens']:
            itens.append(db.getBook(item['rawID']))
    return {'livros': itens}
    


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