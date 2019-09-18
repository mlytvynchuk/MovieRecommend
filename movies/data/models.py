from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=200)
    rating = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

