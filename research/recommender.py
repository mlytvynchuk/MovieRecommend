import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import seaborn as sns
dirname = os.path.dirname(__file__)
warnings.filterwarnings('ignore')

df = pd.read_csv(dirname+'/ratings.csv',
 sep=',', names=['userId', 'movieId','rating','titmestamp'], skiprows=1)


movie_titles = pd.read_csv(dirname+'/movies.csv', sep=',', names=['movieId','title', 'genres'],skiprows=1)
df = pd.merge(df, movie_titles, on='movieId')
# print(df.describe())

ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings['number_of_ratings'] = df.groupby('title')['rating'].count()
# ratings['rating'].hist(bins=50)
# ratings['number_of_ratings'].hist(bins=60)
# sns.jointplot(x='rating', y='number_of_ratings', data=ratings)


movie_matrix = df.pivot_table(index=['userId'], columns=['title', 'genres'], values='rating')
def get_top_rated(ratings):
    return ratings.sort_values('number_of_ratings', ascending=False).head(10)


movie1 = movie_matrix['Dangerous Minds (1995)']
movie2 = movie_matrix['Contact (1997)']


# print(movie1)
# print(movie2)

simular_to_movie1 = movie_matrix.corrwith(movie1)
corr_to_movie1 = pd.DataFrame(simular_to_movie1, columns=['Correlation'])
# drop all null values
corr_to_movie1.dropna(inplace=True)
# print(corr_to_movie1.sort_values('Correlation', ascending=False).head(5))
print(ratings)
# print(simular_to_movie1.sort_values(ascending=False))
# plt.show()

