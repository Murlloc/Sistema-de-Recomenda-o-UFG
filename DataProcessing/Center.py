import db
import DataPreparing as dpre
import DataProcessing as dpro
import ThreadSystem as ts
import numpy as np
import math
import pandas as pd

QTD_DOCUMENTS = 9000000 

try:
    paginadorInicio  = 0
    paginadorFim     = 500000
    dbResponses      = []
    dbResponsesParts = []
    dataFrame        = pd.DataFrame()

    while paginadorInicio <= QTD_DOCUMENTS:
        dbResponse = db.getReviewsOnBooks(paginadorInicio,500000)

        dbResponses = np.append(dbResponses, dbResponse)
        paginadorInicio = paginadorFim
        paginadorFim = paginadorFim + 500000

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
    dpro.predictions(dpre.dataSetCreation(dataFrame))

    

except Exception as e:
	print("ERROR : "+str(e))