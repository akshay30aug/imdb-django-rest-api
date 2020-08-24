from django.urls import include, path
from rest_framework import routers
from movies import views
from django.contrib import admin

router = routers.DefaultRouter()
# router.register(r'watchlist', views.WatchlistViewSet)
router.register(r'movies', views.MovieViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('admin/',admin.site.urls),
    path('addmovies/',views.AddMovies),
    path('watchlist/<pk>/',views.WatchlistView.as_view()),
    path('users/register/',views.UserCreate.as_view()),
    path('user/',views.UserView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]