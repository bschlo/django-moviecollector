from django.db import models

RATINGS = (
   (1, '1'),
   (2, '2'),
   (3, '3'),
   (4, '4'),
   (5, '5')
)

class Actor(models.Model):
   name = models.CharField(max_length=50)
   
   def __string__(self):
      return self.name
   
# Create your models here.
class Movie(models.Model):
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year_made = models.IntegerField()
    actors = models.ManyToManyField(Actor)
    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings.exists():
           return sum(r.rating for r in ratings) / ratings.count()
        return None
    
class Rating(models.Model):
  date = models.DateField('Date Rated')
  rating = models.IntegerField(
     choices=RATINGS, 
     default=1
     )
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

  def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
    return f"{self.get_rating_display()} rating on {self.date}"
  class Meta:
     ordering = ['-rating']


   