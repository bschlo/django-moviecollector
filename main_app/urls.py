from django.urls import path

from .views import Home, MovieList, MovieDetail, RatingListCreate, RatingDetail

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('movies/', MovieList.as_view(), name='movie-list'),
  path('movies/<int:id>/', MovieDetail.as_view(), name='movie-detail'),
  path('movies/<int:movie_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
	path('movies/<int:movie_id>/ratings/<int:id>/', RatingDetail.as_view(), name='rating-detail'),
]
