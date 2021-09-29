import db
import DataPreparing as dpre
import DataProcessing as dpro
import pandas as pd
import ThreadSystem as ts
import numpy as np
import math
QTD_DOCUMENTS = 23000000 

try:
    paginadorInicio  = 0
    paginadorFim     = 2000000
    dbResponses      = []
    dbResponsesParts = []

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
            ts.run(element)
    
    print("Cheguei")

except Exception as e:
	print("ERROR : "+str(e))