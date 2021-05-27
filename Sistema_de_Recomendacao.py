#importing necessary libraries
import numpy as np
import pandas as pd
import math
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from surprise import Reader, Dataset, KNNBasic
from surprise.model_selection import cross_validate
from surprise.model_selection import GridSearchCV
from surprise import SVD

##################################          Parametros       #####################################################

FL_MODELO  = 1
FL_MEMORIA = 0
FL_KNN     = 1
FL_SVD     = 1

USUARIO    = 5

################################## Preparando tabela de Avaliações ###############################################
r_cols = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_csv('./DataSet/u.data2', 
sep='	', names=r_cols, encoding='latin-1')


################################## Preparando tabela de Itens ###############################################
i_cols = ['movie_id', 'title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
          'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
          'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('./DataSet/u.item',  
sep='|', names=i_cols, encoding='latin-1')

ratings_usuario_alvo = []
genero_rating = []
aux = ''
for i in range(len(ratings.values)):
    if (ratings.values[i][0] == USUARIO):
        ratings_usuario_alvo.append({'movie_id': ratings.values[i][1], 
                                    'rating': ratings.values[i][2]})
        if (ratings.values[i][2] > 3):

            for j in range(5,23):
                if(movies.values[ratings.values[i][1] - 1][j] == 1):
                    aux = aux + ' | ' + i_cols[j]

            genero_rating.append({'movie_id': ratings.values[i][1],
                                'movie': movies.values[ratings.values[i][1] - 1][1],
                                'genero': aux })
            aux = ''
count = 0
contador_generos = {'unknown': 0, 'Action': 0, 'Adventure': 0,
          'Animation': 0, 'Children\'s': 0, 'Comedy': 0, 'Crime': 0, 'Documentary': 0, 
          'Drama': 0, 'Fantasy': 0, 'Film-Noir': 0, 'Horror': 0, 'Musical': 0, 
          'Mystery': 0, 'Romance': 0, 'Sci-Fi': 0, 'Thriller': 0, 'War': 0, 'Western': 0}
for i in range(len(genero_rating)):
    genero = genero_rating[i]['genero']
    for j in range(5,23):
        if (i_cols[j] in genero):
            contador_generos[i_cols[j]] = contador_generos[i_cols[j]] + 1

print(contador_generos)

################################## Preparando tabela de Usuarios ###############################################
u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('./DataSet/u.user', 
sep='|', names=u_cols, encoding='latin-1')

################################## Monta a matriz (Usuarios X Itens) ##########################################
X = ratings.copy()
y = ratings['user_id']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, stratify=y, random_state=42)
df_ratings = X_train.pivot(index='user_id', columns='movie_id', values='rating')

ratings = ratings.drop(columns='timestamp')
reader = Reader()
#dataset creation
data = Dataset.load_from_df(ratings, reader)

if (FL_MEMORIA == 1):
    df_ratings_dummy = df_ratings.copy().fillna(0)

    ################################## cosine similarity of the ratings ##################################
    similarity_matrix = cosine_similarity(df_ratings_dummy, df_ratings_dummy)
    ################################## calculate ratings using weighted sum of cosine similarity ##################################
    similarity_matrix_df = pd.DataFrame(similarity_matrix, index=df_ratings.index, columns=df_ratings.index)
    
    def calculate_ratings(id_movie, id_user):
        if id_movie in df_ratings:
            ################################## similarity of id_user with every other user ##################################
            cosine_scores = similarity_matrix_df[id_user] 
            ################################## ratings of every other user for the movie id_movie ##################################
            ratings_scores = df_ratings[id_movie]      
            ################################## won't consider users who havent rated  id_movie so drop similarity scores and ratings corresponsing to np.nan ##################################
            index_not_rated = ratings_scores[ratings_scores.isnull()].index
            ratings_scores = ratings_scores.dropna()
            cosine_scores = cosine_scores.drop(index_not_rated)
            ################################## calculating rating by weighted mean of ratings and cosine scores of the users who have rated the movie ##################################
            ratings_movie = np.dot(ratings_scores, cosine_scores)/cosine_scores.sum()
        else:
            return 2.5
        return ratings_movie

    print('\n')
    ################################## calculate rating by movie_id and user_id ##################################
    print("Wheight approah - Rating by movie_id and user_id: ", calculate_ratings(1,110))

    ################################## evaluation of our wheight model on the test set using root_mean_squared_error ##################################
    def score_on_test_set():
        user_movie_pairs = zip(X_test['movie_id'], X_test['user_id'])
        predicted_ratings = np.array([calculate_ratings(movie, user) for (movie,user) in user_movie_pairs])
        true_ratings = np.array(X_test['rating'])
        score = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
        return score

    print('\n')
    print("Evaluation of our wheight model: ", score_on_test_set())
    print('\n')

if (FL_MODELO == 1 & FL_KNN == 1):
    knn = KNNBasic()
    knn.k = 12
    print('***************************** KNN ****************************************\n')
    print(cross_validate(knn, data, measures=['RMSE', 'mae'], cv = 3))
    print('\n')
    trainset = data.build_full_trainset()
    print(knn.sim)
    print('\n')
    knn.fit(trainset)
    lista = []
    for i in range(df_ratings.head().columns.size):
        predict = knn.predict(USUARIO, i)
        lista.append({'pred': predict.est, 'movie_index': predict.iid})

    def myFunc(e):
        return e['pred']

    lista.sort(key=myFunc, reverse=True)
    top_10 = lista[:10]
    print('\nRecomendações para o usaurio: ' + 'ID - ' +str(users.values[USUARIO - 1][0]) + 
    '. Idade: ' + str(users.values[USUARIO - 1][1]) + '. Sexo: ' + users.values[USUARIO - 1][2] + '\n')
    for i in range(len(top_10)):
        aux = ''
        for j in range(5,23):
                if(movies.values[top_10[i]['movie_index'] - 1][j] == 1):
                    aux = aux + ' | ' + i_cols[j]
        print(str(movies.values[top_10[i]['movie_index'] - 1][0]) + ' - ' + 
            movies.values[top_10[i]['movie_index'] - 1][1] + ' \t\t ' + aux )


if (FL_MODELO == 1 & FL_SVD == 1):
    svd = SVD()
    svd.k = 20
    print('***************************** SVD ****************************************\n')
    print(cross_validate(svd, data, measures=['RMSE'], cv = 3))
    print('\n')
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    lista = []
    print("**** qi *****\n")
    print(svd.qi)
    print("\n**** pu *****\n")
    print(svd.pu)
    for i in range(df_ratings.head().columns.size):
        predict = svd.predict(USUARIO, i)
        lista.append({'pred': predict.est, 'movie_index': predict.iid})

    def myFunc(e):
        return e['pred']

    lista.sort(key=myFunc, reverse=True)
    top_10 = lista[:10]
    print('\nRecomendações para o usaurio: ' + 'ID - ' +str(users.values[USUARIO - 1][0]) + 
    '. Idade: ' + str(users.values[USUARIO - 1][1]) + '. Sexo: ' + users.values[USUARIO - 1][2] + '\n')
    for i in range(len(top_10)):
        aux = ''
        for j in range(5,23):
                if(movies.values[top_10[i]['movie_index'] - 1][j] == 1):
                    aux = aux + ' | ' + i_cols[j]
        print(str(movies.values[top_10[i]['movie_index'] - 1][0]) + ' - ' + 
            movies.values[top_10[i]['movie_index'] - 1][1] + aux)
    print('\nÉ nois')



#TODO -> Codigo - excluir os itens já avaliados
#TODO -> Codigo - pegar os 10 filmes com maiores previsões (.est)

#TODO -> Parte Escrita - Introdução
#TODO -> Parte Escrita - Resumo
#TODO -> Parte Escrita - Estudo de Caso

#TODO -> Parte da Apresentação

    

