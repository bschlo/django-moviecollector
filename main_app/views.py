from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import Movie, Rating, Actor
from .serializers import MovieSerializer, RatingSerializer, ActorSerializer

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
  
  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    # Get the list of toys not associated with this cat
    actors_not_associated = Actor.objects.exclude(id__in=instance.actors.all())
    actors_serializer = ActorSerializer(actors_not_associated, many=True)

    return Response({
        'movie': serializer.data,
        'actors_not_associated': actors_serializer.data
    })

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
  
class ActorList(generics.ListCreateAPIView):
  queryset = Actor.objects.all()
  serializer_class = ActorSerializer

class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Actor.objects.all()
  serializer_class = ActorSerializer
  lookup_field = 'id'

class AddActorToMovie(APIView):
  def post(self, request, movie_id, actor_id):
    movie = Movie.objects.get(id=movie_id)
    actor = Actor.objects.get(id=actor_id)
    movie.actors.add(actor)
    return Response({'message': f'Actor {actor.name} added to Movie {movie.name}'})

class RemoveActorFromMovie(APIView):
  def post(self, request, movie_id, actor_id):
    movie = Movie.objects.get(id=movie_id)
    actor = Actor.objects.get(id=actor_id)
    movie.actors.remove(actor)
    return Response({'message': f'Actor {actor.name} removed from Movie {movie.name}'})
