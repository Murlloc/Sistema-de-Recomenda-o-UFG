#importing necessary libraries
import numpy as np
import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, KNNBasic
from surprise.model_selection import cross_validate
from surprise import SVD

##################################          Parametros       #####################################################

FL_MODELO  = 0
FL_MEMORIA = 1
FL_KNN     = 0
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

if (FL_MEMORIA == 1):
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
    lista = []

    #TODO -> excluir os itens já avaliados
    #TODO -> Ordenar a lista e pegar os 10 filmes com maiores previsões (.est)
    #TODO -> Organizar o metodo baseado em memoria

    for i in range(df_ratings.head().columns.size):
        lista.append(svd.predict(5, i).est)
    lista.sort(reverse=True)
    print('hi')
