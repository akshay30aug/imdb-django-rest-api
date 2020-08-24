from django.contrib.auth.models import User, Group
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from movies.serializers import MovieSerializer, WatchlistSerializer, UserSerializer, UserViewSerializer
from .models import Movie,Watchlist
from bs4 import BeautifulSoup as BS
import requests

class WatchlistView(APIView):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	permission_classes = [permissions.IsAuthenticated]
	def get(self,request,pk):
		try:
			watchlist = self.request.user.watchlist_set.get(pk=pk)
			movieserializer = MovieSerializer(watchlist.movies,many=True)
			return Response(movieserializer.data,status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response(status=status.HTTP_403_FORBIDDEN)
	
	def post(self,request,pk):
		try:
			watchlist = self.request.user.watchlist_set.get(pk=pk)
		except:
			return Response(status=status.HTTP_403_FORBIDDEN)
		try:
			request_type = request.data.get('type')
			if request_type == "add":
				response_text = "Successfully added "
				ids = request.data.getlist('movie_ids')
				moviect = len(ids)
				moviefound = 0
				for i in ids:
					try:
						movie = Movie.objects.get(pk=int(i))
						watchlist.movies.add(movie)
						watchlist.save()
						moviefound += 1
						response_text += movie.name + ", "
					except Exception as e:
						print(e)
						pass
				response_text = response_text[:-2]+" in watchlist."
				if not moviefound == moviect:
					response_text += " But some ids of movies were wrong."
			elif request_type == "del":
				response_text = "Successfully deleted "
				ids = request.data.getlist('movie_ids')
				moviect = len(ids)
				moviefound = 0
				for i in ids:
					try:
						movie = Movie.objects.get(pk=i)
						watchlist.movies.remove(movie)
						watchlist.save()
						moviefound += 1
						response_text += movie.name + ", "
					except Exception as e:
						print(e)
						pass
				response_text = response_text[:-2]+" from watchlist."
				if not moviefound == moviect:
					response_text += " But some ids of movies were wrong."
			else:
				return Response({'error':'post request type '+request_type+' does not exist'},status=status.HTTP_400_BAD_REQUEST)
			return Response({'message':response_text},status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({'message':"post request type not found"},status=status.HTTP_404_NOT_FOUND)

class UserView(APIView):
	"""docstring for UserView"""
	permission_classes = [permissions.IsAuthenticated]
	def get(self,request,format='None'):
		userserializer = UserViewSerializer(request.user)
		movies = request.user.movie_set.all()
		watchlists = request.user.watchlist_set.all()
		watchedserializer = MovieSerializer(movies,many=True)
		watchlistserializer = WatchlistSerializer(watchlists,many=True,context={'request':request})
		return Response({'user-data':userserializer.data,'watched_movies':watchedserializer.data,'watchlist':watchlistserializer.data},status=status.HTTP_200_OK)
	def post(self,request):
		try:
			request_type = request.data.get('type')
			if request_type == "watched_add":
				movie = Movie.objects.get(pk=request.data.get('movie_id'))
				movie.watched.add(User.objects.get(username=request.user.username))
				movie.save()
				response_text = "Successfully added "+movie.name+" in watched."
			elif request_type == "watched_del":
				movie.watched.remove(request.user)
				movie.save()
				response_text = "Successfully deleted "+movie.name+" from watched."
			elif request_type == "watchlist_del":
				watchlist = request.user.watchlist_set.get(pk=request.data.get('watchlist_id'))
				watchlist.delete()
			elif request_type == "watchlist_add":
				watchlist = Watchlist(name=request.data.get('watchlist_name'),created_by=request.user)
				watchlist.save()
				response_text = "Successfully added "
				ids = request.data.getlist('movie_ids')
				moviect = len(ids)
				moviefound = 0
				for i in ids:
					try:
						movie = Movie.objects.get(pk=i)
						watchlist.movies.add(movie)
						watchlist.save()
						moviefound += 1
						response_text += movie.name + ", "
					except Exception as e:
						print(e)
						pass
				response_text = response_text[:-2]+" in watchlist."
				if not moviefound == moviect:
					response_text += " But some ids of movies were wrong."
			else:
				return Response({'error':'post request type '+request_type+' does not exist'},status=status.HTTP_400_BAD_REQUEST)
			return Response({'message':response_text},status=status.HTTP_200_OK)
		except Exception as e:
			print(e)
			return Response({'message':"Wrong/Missing parameters."},status=status.HTTP_404_NOT_FOUND)
		
class UserCreate(APIView):
	""" 
	Creates the user. 
	"""
	permission_classes = [permissions.AllowAny]
	def post(self, request, format='json'):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()
			if user:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	queryset = Movie.objects.all().order_by('id')
	serializer_class= MovieSerializer
	http_methods_names=['get']
	# permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def AddMovies(request):
	"""
	API endpoint that allows groups to be viewed or edited.
	"""
	try:
		print(request.data)
		default_url = 'https://imdb.com'
		url = request.POST.get('url')
		r= requests.get(url)
		soup = BS(r.text,'html.parser')
		table = soup.table
		trs = table.findAll('tr')[1:]
		for i in trs:
			try:
				title = i.find('td',class_='titleColumn').a.text
				rating = i.find('td',class_='imdbRating').strong.text
				year = i.find('td',class_='titleColumn').span.text[1:5]
				murl = i.a['href']
				movie_url = default_url+murl
				movies = Movie.objects.filter(url=movie_url)
				if movies:
					pass
				else:
					res = requests.get(movie_url)
					msoup = BS(res.text,'html.parser')
					image = msoup.find('div',class_='poster').a.img['src']
					plot_summary = msoup.find('div',class_='plot_summary')
					summary = plot_summary.find('div',class_='summary_text').text
					credits = plot_summary.findAll('div',class_='credit_summary_item')
					directors = credits[0].findAll('a')
					director = ""
					for j in directors:
						if "more credit" not in j.text:
							director +=j.text+", "
					writers = credits[1].findAll('a')
					writer = ""
					for j in writers:
						if "more credit" not in j.text:
							writer +=j.text+", "
					topcasts = credits[2].findAll('a')
					topcast = ""
					for j in topcasts[:-1]:
						topcast +=j.text+", "
					director = director[:-2]
					writer = writer[:-2]
					topcast = topcast[:-2]
					m = Movie(name=title,rating=float(rating),year=int(year),directors=director,writers=writer,topcast=topcast,image=image,url=movie_url)
					m.save()
					print(director,writer,topcast)
			except Exception as e:
				print(e,"forloop")
		return Response(status=status.HTTP_201_CREATED)
	except Exception as e:
		print(e)
		return Response(status = status.HTTP_400_BAD_REQUEST)
