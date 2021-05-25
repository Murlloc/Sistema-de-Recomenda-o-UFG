#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, KNNBasic
from surprise.model_selection import cross_validate
from surprise import SVD

r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('/home/murloc/VsCode/Python/TCC/Sistema-de-Recomenda-o-UFG/DataSet/u.data', sep='	', names=r_cols,
encoding='latin-1')
print(ratings.head())

i_cols = ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('/home/murloc/VsCode/Python/TCC/Sistema-de-Recomenda-o-UFG/DataSet/u.item',  sep='|', names=i_cols, encoding='latin-1')
print(movies.head())
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('/home/murloc/VsCode/Python/TCC/Sistema-de-Recomenda-o-UFG/DataSet/u.user', sep='|', names=u_cols,
encoding='latin-1')
print(users.head())

#Assign X as the original ratings dataframe and y as the user_id column of ratings.
X = ratings.copy()
y = ratings['user_id']
#Split into training and test datasets, stratified along user_id
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, stratify=y, random_state=42)

df_ratings = X_train.pivot(index='user_id', columns='movie_id', values='rating')

print('\n\n\n')
print(df_ratings.head())


ratings = ratings.drop(columns='timestamp')
reader = Reader()
#dataset creation
data = Dataset.load_from_df(ratings, reader)

svd = SVD()
trainset = data.build_full_trainset()
svd.fit(trainset)
ratings[ratings['user_id'] == 5]

print(svd.predict(1, 110))