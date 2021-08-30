from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD

def svdRatings(data):
    svd = SVD()
    svd.k = 20
    print('***************************** SVD ****************************************\n')
    print(cross_validate(svd, data, measures=['RMSE'], cv = 6))
    print('\n')
    trainset = data.build_full_trainset()
    return svd.fit(trainset)

def predictions(userID, asin, svd):
    return svd.predict(userID, asin)