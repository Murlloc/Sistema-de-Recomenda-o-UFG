from surprise import Reader, Dataset
from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD

def dataSetCreation(ratingsDF):
    reader = Reader()
    #dataset creation
    return Dataset.load_from_df(ratingsDF, reader)