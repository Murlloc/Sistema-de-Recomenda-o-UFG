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
            list_cur_zero = list(dbResponse)
            df = pd.DataFrame(list_cur_zero)
        else:
            list_cur = list(dbResponse)
            dfAux = pd.DataFrame(list_cur)
            df = pd.concat([df,dfAux], ignore_index=True)
            del dfAux
        paginadorInicio = paginadorFim
        paginadorFim = paginadorFim + 100000

        print(df.count())
        print("\n")
    
    print(dpro.predictions(1, dpre.dataSetCreation(df)))
    
except Exception as e:
	print("ERROR : "+str(e))