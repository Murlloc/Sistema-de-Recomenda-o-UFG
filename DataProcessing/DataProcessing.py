from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD
import db

def predictions(data):
    svd = SVD()
    svd.k = 20
    print('***************************** SVD ****************************************\n')
    #print(cross_validate(svd, data, measures=['RMSE'], cv = 3))
    print('\n')
    trainset = data.build_full_trainset()
    svd.fit(trainset)

    size2     = 0
    itens     = []
    itensQTDE = svd.trainset.n_items

    while size2 < 100:
        size = 0
        user = trainset.to_raw_uid(size2)

        if db.getUser(user) == True:
            size2 = size2 + 1
            continue
            
        while size < itensQTDE:
            itemId = trainset.to_raw_iid(size)
            result = svd.predict(user, itemId)
            item = {
                "_id": size,
                "rawID": result.iid,
                "previsão": result.est
            }
            itens.append(item)
            size = size + 1
        def myFunc(e):
            return e['previsão']
        itens.sort(key=myFunc, reverse=True)
        top_25 = itens[:25]

        userPredictions = {
            "rawID": str(trainset.to_raw_uid(size2)),
            "itens": top_25
        }

        if db.insertBookPrediction(userPredictions) == True:
            print("\n\n")
            print(str(trainset.to_raw_uid(size2)) + " -> Foi add com sucesso")
        else:
            print("error no insert")
        size2 = size2 + 1

"""
usersPredictions 
{
    "_id": 0,
    "rawID": "A1YJFHLJ2TVZ0C",
    "itens": [
        {
            "_id": 0,
            "rawID": "0785214321",
            "previsão": 4.22
        },...
    ]
}
"""