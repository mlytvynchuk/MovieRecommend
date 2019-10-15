from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=50)
    image = models.TextField()
    original = models.CharField(max_length=50)
    description = models.TextField()
    director = models.CharField(max_length=50)
    date = models.CharField(max_length=5)
    actors = models.TextField()
    rating = models.FloatField()
    genre = models.TextField()

    def __str__(self):
        return self.title
    

