import queue
from threading import Thread
from time import sleep
import pandas as pd

def toDataFrame(data):
    list_cur_zero = list(data)
    df = pd.DataFrame(list_cur_zero)
    return df

def run(DBdata):

    que = queue.Queue()
    threads_list = list()

    for element in DBdata:
        t = Thread(target=lambda q, arg1: 
            q.put(toDataFrame(arg1)), args=(que, element))
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

    aux = pd.DataFrame()
    while not que.empty():
        result = que.get()
        aux = pd.concat([aux,result], ignore_index=True)
    return aux