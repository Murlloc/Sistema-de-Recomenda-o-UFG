import pandas as pd
import numpy as np

# Libraries for Recommendation System
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

r_cols = ['userId', 'movieId', 'rating']

ratings = pd.read_csv('./DataSet/ratings.csv')

data_movie = pd.read_csv("./DataSet/movies.csv")
data_rating = pd.read_csv("./DataSet/ratings.csv")

movie = data_movie.loc[:,{"movieId","title"}]
rating = data_rating.loc[:,{"userId","movieId","rating"}]

print(movie.head())
print(rating.head())

print('----------------------------------------------------')

data = pd.merge(movie,rating)
data = data.iloc[:1000000,:]
user_movie_table = data.pivot_table(index = ["title"],columns = ["userId"],values = "rating").fillna(0)

print(user_movie_table.head(10))
print('----------------------------------------------------')

query_index = np.random.choice(user_movie_table.shape[0])
print("Choosen Movie is: ",user_movie_table.index[query_index])

user_movie_table_matrix = csr_matrix(user_movie_table.values)
model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(user_movie_table_matrix)
distances, indices = model_knn.kneighbors(user_movie_table.iloc[query_index,:].
values.reshape(1,-1), n_neighbors = 6)

movie = []
distance = []

for i in range(0, len(distances.flatten())):
    if i != 0:
        movie.append(user_movie_table.index[indices.flatten()[i]])
        distance.append(distances.flatten()[i])    

m=pd.Series(movie,name='movie')
d=pd.Series(distance,name='distance')
recommend = pd.concat([m,d], axis=1)
recommend = recommend.sort_values('distance',ascending=False)

print('Recommendations for {0}:\n'.format(user_movie_table.index[query_index]))
for i in range(0,recommend.shape[0]):
    print('{0}: {1}, with distance of {2}'.format(i, recommend["movie"].iloc[i], recommend["distance"].iloc[i]))