from django.db import models


# Create your models here.
class MaoyanMovie(models.Model):
    name = models.CharField(max_length=200)
    stars = models.CharField(max_length=200)
    release_time = models.DateField(max_length=30)
    score = models.FloatField(max_length=10)
