import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from .models import Movie

def run(data, target_movie):
    begin = time.time()
    df = data
    features = ['keywords', 'actors', 'genre', 'director']
    # drop empty
    # for feature in features:
    #     df[feature] = df[feature].fillna('')  # replace none by emty string
    
    df["combined_features"] = df.apply(combine_features, axis=1)
    # make vectorizer
    cv = CountVectorizer()

    count_matrix = cv.fit_transform(df['combined_features'])
    cosine_sim = cosine_similarity(count_matrix)
    return find_simulars(target_movie,cosine_sim, df)


def combine_features(row):
    return row['keywords']+' '+row['actors']+" "+row['genre']+' '+row['director']


def find_simulars(movie_user_likes,cosine_sim,df):
    sim_movies = []
    movie_index = movie_user_likes.pk-1
    if movie_index:
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(
            similar_movies, key=lambda x: x[1], reverse=True)[1:]

        i = 0

        for element in sorted_similar_movies:
            sim_movie = Movie.objects.get(pk=element[0]+1)
            sim_movies.append(sim_movie)
            i = i+1
            if i >= 5:
                break
    return sim_movies
