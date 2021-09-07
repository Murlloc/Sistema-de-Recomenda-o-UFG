import db
import DataPreparing as dpre
import DataProcessing as dpro
import pandas as pd

QTD_DOCUMENTS = 1000000 #MAX = 23000000 

try:
    paginadorInicio = 0
    paginadorFim    = 1000000

    while paginadorInicio != QTD_DOCUMENTS:
        dbResponse = db.getReviewsOnBooks(paginadorInicio,paginadorFim)
        if paginadorInicio == 0:
            df = pd.DataFrame(dbResponse)
        else:
            dfAux = pd.DataFrame(dbResponse)
            df = pd.concat([df,dfAux], ignore_index=True)
            del dfAux
        paginadorInicio = paginadorFim
        paginadorFim = paginadorFim + 100000

        print(df.count())
        print("\n")
    
    print(dpro.predictions(1, dpre.dataSetCreation(df)))
    
except:
    print("Deu ruim na leitura")