from django.contrib import admin
# import your models here
from .models import Movie, Rating

# Register your models here
admin.site.register(Movie)
admin.site.register(Rating)