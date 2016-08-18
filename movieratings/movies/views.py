from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import Movie, Rater, Rating
from django.http import Http404
from django.db.models import Avg


# Create your views here.
def index(request):
    # all_ratings = {}
    m = Movie.objects.all()
    for movie in m:
        avg_rate = Movie.objects.aggregate(average_rating=Avg('rating__score'))

        # ratings = movie.rating_set.all()
        # ratings = [rating.score for rating in ratings]
        # if len(ratings) > 0:
        #     avg_rating = sum(ratings)/len(ratings)
        all_ratings[movie.id] = avg_rate
    context = {
        'Movies': m,
        'Avg_rating': all_ratings,
        # 'Avg_rate': avg_rate,
        }
    return render(request, 'movies/index.html', context)


def movie_view(request):
    all_movies = Movie.objects.all()
    context = {
        'all_movies': all_movies,
    }
    return render(request, 'movies/movie_view.html', context)


def movie_detail(request, movie_id):
    avg_rate = Movie.objects.aggregate(average_rating=Avg('rating__score'))
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        raise Http404("Movie doesn't exist")
    context = {
        'movie': movie,
        'avg_rate': avg_rate,
    }
    return render(request, 'movies/movie_detail.html', context)


def user_view(request):
    all_raters = Rater.objects.all()
    context = {
        'all_raters': all_raters,
    }
    return render(request, 'movies/user_view.html', context)


def user_detail(request, rater_id):
    try:
        rater = Rater.objects.get(pk=rater_id)
    except Rater.DoesNotExist:
        raise Http404("Rater doesn't exist")
    context = {
        'rater': rater,
    }
    return render(request, 'movies/user_detail.html', context)
