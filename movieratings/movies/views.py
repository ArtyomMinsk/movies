from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import Movie, Rater, Rating


# Create your views here.
def index(request):
    all_ratings = {}
    m = Movie.objects.all()
    for movie in m:
        ratings = movie.rating_set.all()
        ratings = [rating.score for rating in ratings]
        if len(ratings) > 0:
            avg_rating = sum(ratings)/len(ratings)
        all_ratings[movie.id] = avg_rating
    context = {
        'Movies': m,
        'Avg_rating': all_ratings,
    }

    return render(request, 'movies/index.html', context)


def movie_view(request):
    movies = Movie.objects.all()
    context = {
        'Movies': movies,
    }
    return render(request, 'movies/movie_view.html', context)


def user_view(request):
    users = Rater.objects.all()
    context = {
        'Users': users,
    }
    return render(request, 'movies/user_view.html', context)
