from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the movie-collector api home route!'}
    return Response(content)
  
class MovieList(generics.ListCreateAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Movie.objects.all()
  serializer_class = MovieSerializer
  lookup_field = 'id'

class RatingListCreate(generics.ListCreateAPIView):
  serializer_class = RatingSerializer

  def get_queryset(self):
    movie_id = self.kwargs['movie_id']
    return Rating.objects.filter(movie_id=movie_id)

  def perform_create(self, serializer):
    movie_id = self.kwargs['movie_id']
    movie = Movie.objects.get(id=movie_id)
    serializer.save(movie=movie)

class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = RatingSerializer
  lookup_field = 'id'

  def get_queryset(self):
    movie_id = self.kwargs['movie_id']
    return Rating.objects.filter(movie_id=movie_id)
  


  