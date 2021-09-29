import db
import DataPreparing as dpre
import DataProcessing as dpro
import ThreadSystem as ts
import numpy as np
import math
import pandas as pd

QTD_DOCUMENTS = 23000000 

try:
    paginadorInicio  = 0
    paginadorFim     = 2000000
    dbResponses      = []
    dbResponsesParts = []
    dataFrame        = pd.DataFrame()

    while paginadorInicio <= QTD_DOCUMENTS:
        dbResponse = db.getReviewsOnBooks(paginadorInicio,paginadorFim)
        dbResponses = np.append(dbResponses, dbResponse)
        paginadorInicio = paginadorFim
        paginadorFim = paginadorFim + 2000000

    if len(dbResponses) > 1:
        numberOfTimes = math.ceil(len(dbResponses)/6)
        aux1 = 0
        aux2 = 6
        for count in range(numberOfTimes):
            dbResponsesParts.append(dbResponses[aux1:aux2])
            aux1 = aux2
            aux2 = aux2 + 7
        for element in dbResponsesParts:
            aux = ts.run(element)
            dataFrame = pd.concat([dataFrame,aux], ignore_index=True)

    print(dataFrame.count())
    dataSet = dpre.dataSetCreation(dataFrame)
    svd = dpro.svdRatings(dataSet)

    

except Exception as e:
	print("ERROR : "+str(e))