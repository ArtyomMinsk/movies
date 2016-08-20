from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .forms import RaterForm, RatingForm
from .models import Movie, Rater, Rating
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
    print("MOVIE: ", movie)
    search = youtube_search(movie.title + 'trailer')
    first_result = search[0]

    rating_form = None
    if request.user.is_authenticated():
        rater = request.user.rater
        user_rating = rater.get_score_for_movie(movie)
        print("USER RATING: ", user_rating)

        rating_form = RatingForm(request.POST)

        if user_rating:
            # User is logged in and has rated the movie
            user_display = "You gave this movie a {}.".format(
                                                        user_rating.score)
        else:
            # User is logged in, but has not rated the movie
            user_display = "Click here to rate this movie."

        if rating_form.is_valid():
            print("Rating Form is Valid")
            score = rating_form.cleaned_data['score']
            review = rating_form.cleaned_data['review']
            if user_rating:
                print("User editing existing rating")
                # Edit the existing rating
                user_rating.score = score
                user_rating.review = review
                user_rating.timestamp = timezone.now()
                user_rating.save()
            else:
                # Add a new rating for this user
                print("New rating for unrated movie")

                print("PRINT THIS ", rating_form)
                user_rating = Rating(score=score, rater=rater,
                                     movie=movie, review=review)
                # user_rating = rating_form.save(commit=False)
                user_rating.save()

        else:
            print(rating_form)
            print("invalid input")

    else:
        # User is not logged in
        user_display = "Login to rate this movie."

    try:
        movie = Movie.objects.get(pk=movie_id)
        average_score = movie.get_average_score()
    except Movie.DoesNotExist:
        raise Http404("Movie doesn't exist")
    context = {
        'search': first_result,
        'movie': movie,
        'average_score': '{0:.2f}'.format(average_score),
        'user_display': user_display,
        'rating_form': rating_form,
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
    for rater in others:
        rater = Rater.objects.get(pk=2)
        set2 = rater.rating_set.all()
        common1 = set1.filter(
                movie_id__in=[m.movie_id for m in set2]).order_by('movie_id')
        common2 = set2.filter(
                movie_id__in=[m.movie_id for m in set1]).order_by('movie_id')
        euclid = Rater.euclidean_distance(common1, common2)
        break
    context = {
        'user_ratings': set1,
        'rater_ratings': set2,
        'common1': common1,
        'common2': common2,
        'euclid': euclid,
    }
    return render(request, 'movies/movies_for_you.html', context)
