from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import Movie, Rater, Rating
from django.http import Http404
from django.db.models import Avg


# Create your views here.
def index(request):
    top_twenty = Movie.get_average_scores()
    context = {
        'Movies': top_twenty,
        }
    return render(request, 'movies/index.html', context)


def movie_view(request):
    all_movies = Movie.objects.all()
    context = {
        'all_movies': all_movies,
    }
    return render(request, 'movies/movie_view.html', context)


def movie_detail(request, movie_id):
    avg_rate = Movie.get_average_score(movie_id)
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
