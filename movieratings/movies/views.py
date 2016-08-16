from django.shortcuts import render
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    pass


def logout_view(request):
    pass


def login_view(request):
    if request.GET:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
        else:
            pass
            # Return an 'invalid login' error message.

    # return render(request, 'movies/index.html')


def movie_view(request):
    pass


def user_view(request):
    pass
