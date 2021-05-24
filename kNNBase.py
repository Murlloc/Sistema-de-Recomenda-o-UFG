import pandas as pd
import numpy as np

r_cols = ['user_id', 'movie_id', 'rating']

ratings = pd.read_csv('./dataSetBase/u.data', sep='\t', names=r_cols, usecols=range(3))

movieProperties = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
movieNumRatings = pd.DataFrame(movieProperties['rating']['size'])
movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))


print(movieNormalizedNumRatings.head())
print("------------------------------")

movieDict = {}

with open(r'./dataSetBase/u.item', encoding="ISO-8859-1") as f:
    temp = ''
    for line in f:
        #line.encode().decode("ISO-8859-1")
        fields = line.rstrip('\n').split('|')
        movieID = int(fields[0])
        name = fields[1]
        genres = fields[5:25]
        genres = map(int, genres)
        movieDict[movieID] = ('name: ${name}', np.array(list(genres)), movieNormalizedNumRatings.loc[movieID].get('size'), movieProperties.loc[movieID].rating.get('mean'))

print(movieDict[1])