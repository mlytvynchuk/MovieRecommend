from django.shortcuts import render
from .models import Movie
# Create your views here.

def index(request):
    if request.method == "GET":
        movies = Movie.objects.all()
        return render(request, 'movies/index.html', {'movies': movies})
