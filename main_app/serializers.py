from rest_framework import serializers
from .models import Movie, Rating, Actor

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()   
    actors = ActorSerializer(many=True, read_only=True)
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

      

