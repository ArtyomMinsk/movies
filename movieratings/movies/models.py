from django.db import models
from django.db.models import Count, Avg
from django.contrib.auth.models import User
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=500)

    def __str__(self):
        return "{}: {} {}".format(self.id, self.title, self.genre)

    def get_average_score(self):
        if len(self.rating_set.all()) > 0:
            return self.rating_set.all().aggregate(Avg('score'))['score__avg']
        else:
            return "Has not been rated"

    def get_average_scores(n=20):
            return Movie.objects.annotate(
                num_ratings=Count('rating')).filter(
                num_ratings__gt=10).annotate(
                average_rating=Avg('rating__score')).values(
                        'id',
                        'title',
                        'genre',
                        'average_rating').order_by('-average_rating')[:n]


class Rater(models.Model):
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    occupation = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    user = models.OneToOneField(User)

    def __str__(self):
        return "{}. Age:{} Gender:{}".format(self.id, self.age, self.gender)

    def get_average_score(self):
        if len(self.rating_set.all()) > 0:
            return self.rating_set.all().aggregate(Avg('score'))['score__avg']
        else:
            return "Has not been rated"

    def get_average_scores(n=20):
        return Rater.objects.annotate(
            num_ratings=Count('rating')).filter(
            num_ratings__gt=10).annotate(
            average_rating=Avg('rating__score')).values(
                'id', 'average_rating').order_by('-average_rating')[:n]

    def get_score_for_movie(self, movie):
        """Returns None if they have not rated the movie
           Returns a rating object if they have rated the movie"""
        try:
            score = Rating.objects.get(movie=movie, rater=self)
        except:
            return None
        else:
            return score

    def euclidean_distance(v, w):
        if len(v) is 0:
            return 0

        differences = [v[idx].score - w[idx].score for idx in range(len(v))]
        squares = [diff ** 2 for diff in differences]
        sum_of_squares = sum(squares)

        return 1/(1 + (sum_of_squares ** 0.5))


class Rating(models.Model):
    CHOICES = [(i, i) for i in range(1, 6)]
    timestamp = models.DateTimeField(default=timezone.now)
    score = models.IntegerField(choices=CHOICES)
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    review = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.movie.title, self.score)
