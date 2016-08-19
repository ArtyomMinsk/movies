from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm



from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^movie/$', views.movie_view, name='movie_view'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$',
        views.movie_detail, name='movie_detail'),
    url(r'^rater/$', views.user_view, name='user_view'),
    url(r'^rater/(?P<rater_id>[0-9]+)/$',
        views.user_detail, name='user_detail'),
    url(r'^register/', CreateView.as_view(template_name='registration/register.html',
                                          form_class=UserCreationForm,
                                          success_url='/'
                                          )),
]




# For reference from: https://docs.djangoproject.com/en/1.10/intro/tutorial03/
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
