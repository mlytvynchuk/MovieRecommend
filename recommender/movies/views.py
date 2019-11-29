from django.shortcuts import render, render_to_response
from .models import Movie
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from .movie_recommender import run as find_simular_movies
import pandas as pd
from django.template.context import RequestContext
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string


def index(request):
    if request.method == "GET":
        movies = Movie.objects.filter(date=2019).order_by('-rating')[:7]
        return render(request, 'movies/index.html', {'movies': movies})

def details(request, id):
    if request.method == "GET":
        movie = Movie.objects.filter(pk=id)[0]
        actors = movie.actors.split(',')
        return render(request, 'movies/details.html', {'movie': movie, 'actors': actors})


def load_simular_movies(request, id):
    df = pd.DataFrame(list(Movie.objects.all().values()))
    movie = Movie.objects.filter(pk=id)[0]
    print(id)
    simular_movies = find_simular_movies(df, movie)
    rendered = render_to_string('movies/simular_movies.html',context={'simular_movies': simular_movies})
    response = {'data':rendered}
    return JsonResponse(response)
