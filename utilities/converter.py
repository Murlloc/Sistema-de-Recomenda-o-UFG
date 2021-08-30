import csv 
import json
import time

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    linhas = 0
    pagina = 2
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
            linhas = linhas + 1

            if (linhas > 500000):
                with open(jsonFilePath + '_' + str(pagina) + '.json', 'w', encoding='utf-8') as jsonf: 
                    jsonString = json.dumps(jsonArray, indent=4)
                    jsonf.write(jsonString)
                pagina = pagina + 1
                jsonArray = []
                linhas = 0

            print(str(linhas))
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath + '_Ultima' + '.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)
          
csvFilePath = './DataSet/ratings_Books.csv'
jsonFilePath = './DataSet/ratings_Books'

start = time.perf_counter()
csv_to_json(csvFilePath, jsonFilePath)
finish = time.perf_counter()

print(f"Conversion 100.000 rows completed successfully in {finish - start:0.4f} seconds")