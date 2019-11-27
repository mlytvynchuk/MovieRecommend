from django.shortcuts import render
from .models import Movie
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time


def index(request):
    if request.method == "GET":
        movies = Movie.objects.filter(date=2019).order_by('-rating')[:7]
        return render(request, 'movies/index.html', {'movies': movies})

def details(request, id):
    if request.method == "GET":
        movie = Movie.objects.filter(pk=id)[0]
        actors = movie.actors.split(',')
        find_movie_simlar(movie)

        return render(request, 'movies/details.html', {'movie': movie, 'actors': actors})


def combine_features(movie):
        return movie.keywords+ ' ' + movie.actors + ' ' + movie.genre + ' ' + movie.director

def find_movie_simlar(movie):
    cv = CountVectorizer()
    combined_features = combine_features(movie)
    count_matrix = cv.fit_transform(combined_features)
    cosine_sim = cosine_similarity(count_matrix)

    

    def find_simulars(movie_user_likes):
        titles = []
        movie_index = movie_user_likes.pk
        if movie_index:
            similar_movies =  list(enumerate(cosine_sim[movie_index]))
            sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]

            i=0
            print("Top 5 similar movies to "+movie_user_likes+" are:\n")
            for element in sorted_similar_movies:
                print(get_title_from_index(element[0]))
                titles.append(get_title_from_index(element[0]))
                i=i+1
                if i>=5:
                    break
        return titles

    find_simulars(movie.title)