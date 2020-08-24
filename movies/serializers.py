from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Movie,Watchlist


class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
			required=True,
			validators=[UniqueValidator(queryset=User.objects.all())]
			)
	username = serializers.CharField(
			validators=[UniqueValidator(queryset=User.objects.all())]
			)
	password = serializers.CharField(min_length=8)

	def create(self, validated_data):
		user = User.objects.create_user(validated_data['username'], validated_data['email'],
			 validated_data['password'])
		return user

	class Meta:
		model = User
		fields = ['email','username','password']

class UserViewSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username', 'email']

class WatchlistSerializer(serializers.ModelSerializer):
	class Meta:
		model = Watchlist
		fields = ['id','name', 'movies', 'created_by']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Movie
		ordering = ['id']
		fields = ['id','name', 'rating','year','directors','writers','topcast']