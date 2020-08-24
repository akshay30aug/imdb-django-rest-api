from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
	url = models.TextField(db_index=True)
	name = models.CharField(max_length=100)
	rating = models.FloatField(blank=True)
	year = models.IntegerField()
	image = models.TextField(blank=True)
	directors = models.TextField(blank=True)
	writers = models.TextField(blank=True)
	topcast = models.TextField(blank=True)
	watched = models.ManyToManyField(User)
	def __str__(self):
		return self.name

class Watchlist(models.Model):
	name = models.CharField(max_length=100)
	movies = models.ManyToManyField(Movie)
	created_by = models.ForeignKey(User,on_delete=models.CASCADE)
