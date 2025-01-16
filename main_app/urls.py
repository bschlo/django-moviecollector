from django.urls import path

from .views import Home, MovieList, MovieDetail, RatingListCreate, RatingDetail, ActorList, ActorDetail, AddActorToMovie, RemoveActorFromMovie, CreateUserView, LoginView, VerifyUserView

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('movies/', MovieList.as_view(), name='movie-list'),
  path('movies/<int:id>/', MovieDetail.as_view(), name='movie-detail'),
  path('movies/<int:movie_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
	path('movies/<int:movie_id>/ratings/<int:id>/', RatingDetail.as_view(), name='rating-detail'),
  path('actors/', ActorList.as_view(), name='actor-list'),
  path('actors/<int:id>/', ActorDetail.as_view(), name='actor-detail'),
  path('movies/<int:movie_id>/add_actor/<int:actor_id>/', AddActorToMovie.as_view(), name='add-actor-to-movie'),
  path('movies/<int:movie_id>/remove_actor/<int:actor_id>/', RemoveActorFromMovie.as_view(), name='remove-actor-from-movie'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
]
