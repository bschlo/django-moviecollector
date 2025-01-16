from rest_framework import serializers
from .models import Movie, Rating, Actor
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
      user = User.objects.create_user(
          username=validated_data['username'],
          email=validated_data['email'],
          password=validated_data['password']  # Ensures the password is hashed correctly
      )
      
      return user

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()   
    actors = ActorSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'
    
    def get_average_rating(self, obj):
        ratings = obj.rating_set.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return None
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('movie',)

      

