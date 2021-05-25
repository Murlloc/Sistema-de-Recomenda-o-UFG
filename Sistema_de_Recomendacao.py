#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, KNNBasic
from surprise.model_selection import cross_validate
from surprise import SVD

##################################          Parametros       #####################################################

FL_MODELO  = 1
FL_MEMORIA = 0
FL_KNN     = 1
FL_SVD     = 1

################################## Preparando tabela de Avaliações ###############################################
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('./DataSet/u.data', 
sep='	', names=r_cols, encoding='latin-1')

print(ratings.head()) #Amostra

################################## Preparando tabela de Itens ###############################################
i_cols = ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
          'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
          'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('./DataSet/u.item',  
sep='|', names=i_cols, encoding='latin-1')

print(movies.head()) #Amostra

################################## Preparando tabela de Usuarios ###############################################
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('./DataSet/u.user', 
sep='|', names=u_cols, encoding='latin-1')

print(users.head()) #Amostra

################################## Monta a matriz (Usuarios X Itens) ##########################################
X = ratings.copy()
y = ratings['user_id']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, stratify=y, random_state=42)
df_ratings = X_train.pivot(index='user_id', columns='movie_id', values='rating')

print(df_ratings.head()) #Amostra


ratings = ratings.drop(columns='timestamp')
reader = Reader()
#dataset creation
data = Dataset.load_from_df(ratings, reader)

if (FL_MODELO == 1 & FL_KNN == 1):
    knn = KNNBasic()
    print(cross_validate(knn, data, measures=['RMSE', 'mae'], cv = 3))

    trainset = data.build_full_trainset()

    knn.fit(trainset)

    print(knn.predict(5, 2))

if (FL_MODELO == 1 & FL_SVD == 1):
    svd = SVD()

    print(cross_validate(svd, data, measures=['RMSE'], cv = 3))

    trainset = data.build_full_trainset()
    svd.fit(trainset)

    print(svd.predict(5, 2))