from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from .models import Movie, Rating, Actor
from .serializers import MovieSerializer, RatingSerializer, ActorSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied

# include the registration, login, and verification views below
# User Registration
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the movie-collector api home route!'}
    return Response(content)
  
class MovieList(generics.ListCreateAPIView):
  serializer_class = MovieSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      # This ensures we only return cats belonging to the logged-in user
      user = self.request.user
      return Movie.objects.filter(user=user)

  def perform_create(self, serializer):
      # This associates the newly created cat with the logged-in user
      serializer.save(user=self.request.user)

class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = MovieSerializer
  lookup_field = 'id'

  def get_queryset(self):
    user = self.request.user
    return Movie.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    actors_not_associated = Actor.objects.exclude(id__in=instance.actors.all())
    actors_serializer = ActorSerializer(actors_not_associated, many=True)

    return Response({
        'movie': serializer.data,
        'actors_not_associated': actors_serializer.data
    })

  def perform_update(self, serializer):
    cat = self.get_object()
    if cat.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to edit this cat."})
    serializer.save()

  def perform_destroy(self, instance):
    if instance.user != self.request.user:
        raise PermissionDenied({"message": "You do not have permission to delete this cat."})
    instance.delete()


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
