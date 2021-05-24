import pandas as pd
import numpy as np

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