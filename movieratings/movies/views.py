from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .forms import RaterForm
from .models import Movie, Rater
from .youtube import youtube_search


def index(request):
    all_movies_scores = Movie.get_average_scores(10000)
    context = {
        'movies': all_movies_scores
    }
    return render(request, 'movies/index.html', context)


def movie_view(request):
    all_movies = Movie.objects.all()
    context = {
        'all_movies': all_movies,
    }
    return render(request, 'movies/movie_view.html', context)


def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    search = youtube_search(movie.title + 'trailer')
    first_result = search[0]
    try:
        movie = Movie.objects.get(pk=movie_id)
        average_score = movie.get_average_score()
    except Movie.DoesNotExist:
        raise Http404("Movie doesn't exist")
    context = {
        'search': first_result,
        'movie': movie,
        'average_score': '{0:.2f}'.format(average_score),
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


def register_user(request):
    if request.method == 'POST':
        rf = RaterForm(request.POST, prefix='rater')
        uf = UserCreationForm(request.POST, prefix='user')
        if rf.is_valid() * uf.is_valid():
            user = uf.save(commit=False)
            user.save()
            rater = rf.save(commit=False)
            rater.user_id = user.id
            rater.id = user.id
            rater.save()
            user = authenticate(username=uf.cleaned_data['username'],
                                password=uf.cleaned_data['password1'],
                                )
            login(request, user)
            return HttpResponseRedirect(reverse('movies:index'))
    else:
        rf = RaterForm(prefix='rater')
        uf = UserCreationForm(prefix='user')
    context = {'raterform': rf, 'userform': uf}
    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('movies:index'))


def test_table(request):
    # Inspiration: https://datatables.net/examples/styling/bootstrap.html
    all_movies_scores = Movie.get_average_scores(10000)
    context = {
        'movies': all_movies_scores
    }
    return render(request, 'movies/test_table.html', context)


@login_required
def movies_for_you(request):
    user = request.user
    set1 = user.rater.rating_set.all()
    # others = Rater.objects.filter(id__ne=user.rater.id)
    others = Rater.objects.all().exclude(id=user.rater.id)
    euclid_list = []
    for rater in others:
        set2 = rater.rating_set.all()
        common1 = set1.filter(movie_id__in=[m.movie_id for m in set2]).order_by('movie_id')
        common2 = set2.filter(movie_id__in=[m.movie_id for m in set1]).order_by('movie_id')
        euclid = Rater.euclidean_distance(common1, common2)
        euclid_list.append((euclid, rater))
    sorted_list = sorted(euclid_list, key=lambda x: x[0], reverse=True)[:5]
    movie_recs = []
    for user_tuple in sorted_list:
        rater = user_tuple[1]
        ratings = rater.rating_set.all()
        for rating in ratings:
            if set1.filter(movie_id=rating.movie_id):
                pass
            else:
                euclid_rating = (rating.score * user_tuple[0], Movie.objects.get(id=rating.movie_id))
                movie_recs.append(euclid_rating)
    movie_list = sorted(movie_recs, key=lambda x: x[0], reverse=True)[:10]

    context = {
        'movie_list': movie_list,
    }
    return render(request, 'movies/movies_for_you.html', context)
