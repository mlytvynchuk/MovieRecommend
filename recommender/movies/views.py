from django.shortcuts import render
from .models import Movie
# Create your views here.
def index(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        return render(request, 'movies/index.html', {'movies': movies})

def details(request, id):
    if request.method == "GET":
        movie = Movie.objects.filter(pk=id)[0]
        actors = movie.actors.split(',')
        return render(request, 'movies/details.html', {'movie': movie, 'actors': actors})
