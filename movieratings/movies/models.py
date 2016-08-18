from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from statistics import mean

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=500)

    def __str__(self):
        return "{}: {} {}".format(self.id, self.title, self.genre)

    def get_average_score(self):
        return mean([rating.score for rating in self.rating_set.all()])    


class Rater(models.Model):
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1)
    occupation = models.CharField(max_length=200) # TODO: Make sure our migration accounts for this.
    zip_code = models.CharField(max_length=10)
    user = models.OneToOneField(User)

    def __str__(self):
        return "{}. Age:{} Gender:{}".format(self.id, self.age, self.gender)

    def get_average_score(self):
        return mean([rating.score for rating in self.rating_set.all()])


class Rating(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    score = models.IntegerField()
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)

    def __str__(self):
        return "{}: {}".format(self.movie.title, self.score)
