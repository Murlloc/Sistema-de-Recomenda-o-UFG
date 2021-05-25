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
ratings = pd.read_csv('./DataSet/u.data', sep='	', names=r_cols,
encoding='latin-1')
print(ratings.head())

i_cols = ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('./DataSet/u.item',  sep='|', names=i_cols, encoding='latin-1')
print(movies.head())
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('./DataSet/u.user', sep='|', names=u_cols,
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

df_ratings_dummy = df_ratings.copy().fillna(0)
df_ratings_dummy.head()
#cosine similarity of the ratings
similarity_matrix = cosine_similarity(df_ratings_dummy, df_ratings_dummy)
similarity_matrix_df = pd.DataFrame(similarity_matrix, index=df_ratings.index, columns=df_ratings.index)
#calculate ratings using weighted sum of cosine similarity
#function to calculate ratings
def calculate_ratings(id_movie, id_user):
    if id_movie in df_ratings:
        cosine_scores = similarity_matrix_df[id_user] #similarity of id_user with every other user
        ratings_scores = df_ratings[id_movie]      #ratings of every other user for the movie id_movie
        #won't consider users who havent rated id_movie so drop similarity scores and ratings corresponsing to np.nan
        index_not_rated = ratings_scores[ratings_scores.isnull()].index
        ratings_scores = ratings_scores.dropna()
        cosine_scores = cosine_scores.drop(index_not_rated)
        #calculating rating by weighted mean of ratings and cosine scores of the users who have rated the movie
        ratings_movie = np.dot(ratings_scores, cosine_scores)/cosine_scores.sum()
    else:
        return 2.5
    return ratings_movie


print('\n\n\n')
print(calculate_ratings(5,2))

def score_on_test_set():
    user_movie_pairs = zip(X_test['movie_id'], X_test['user_id'])
    predicted_ratings = np.array([calculate_ratings(movie, user) for (movie,user) in user_movie_pairs])
    true_ratings = np.array(X_test['rating'])
    score = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
    return score

print('\n\n')
print(score_on_test_set())