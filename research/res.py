import pandas as pd
import numpy as np
import os
import warnings


dirname = os.path.dirname(__file__)
warnings.filterwarnings('ignore')


data = pd.read_csv(dirname+'/movies.csv', sep=',', names=['movieId','title', 'genres'],skiprows=1)
user_ratings = pd.read_csv(dirname+'/ratings.csv',sep=',')
ratings = pd.DataFrame(user_ratings.groupby('movieId')['rating'].mean())
data = pd.merge(data, ratings, on='movieId')
movie_matrix = data.pivot_table(index='rating', columns=['title', 'genres'], values='movieId')
movie_watched = movie_matrix['Sabrina (1995)']
recommend_list = movie_matrix.corrwith(movie_watched)
recommend_list = pd.DataFrame(recommend_list, columns=['Correlation'])
recommend_list.dropna(inplace=True)

print(recommend_list.head(10))