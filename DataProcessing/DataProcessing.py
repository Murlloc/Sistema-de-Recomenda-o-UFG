from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD

def svdRatings(data):
    svd = SVD()
    svd.k = 20
    print('***************************** SVD ****************************************\n')
    print(cross_validate(svd, data, measures=['RMSE'], cv = 3))
    print('\n')
    trainset = data.build_full_trainset()
    return svd.fit(trainset)

def predictions(userID, data):

    svd = SVD()
    svd.k = 5
    print('***************************** SVD ****************************************\n')
    #print(cross_validate(svd, data, measures=['RMSE'], cv = 3))
    print('\n')
    trainset = data.build_full_trainset()
    svd.sim_options['user_based'] = False
    svd.fit(trainset)

    size = 0
    itens = []
    itensQTDE = svd.trainset.n_items
    userPrediction = {
        "_id": userID,
        "rawID": "",
        "itens": []
    }
    while size < itensQTDE:
        result = svd.predict(userID, size)
        item = {
            "_id": result.iid,
            "rawID": svd.trainset.to_raw_iid(result.iid),
            "previsão": result.est
        }
        itens.append(item)
        print(item)
        size = size + 1

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