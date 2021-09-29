import queue
from threading import Thread
from time import sleep

def toDataFrame(data):
    return 'bar'

def run(DBdata):

    que = queue.Queue()
    threads_list = list()

    for element in DBdata:

        threads_list.append(Thread(target=lambda q, arg1: 
            q.put(toDataFrame(arg1)), args=(que, element)))

    # Add more threads here
    ...
    t2 = Thread(target=lambda q, arg1: q.put(toDataFrame(arg1)), args=(que, 'world2!'))
    t2.start()
    threads_list.append(t2)
    ...
    t3 = Thread(target=lambda q, arg1: q.put(toDataFrame(arg1)), args=(que, 'world3!'))
    t3.start()
    threads_list.append(t3)
    ...

    # Join all the threads
    for t in threads_list:
        t.join()

    # Check thread's return value
    while not que.empty():
        result = que.get()
        print(result)