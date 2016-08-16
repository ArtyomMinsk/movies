from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^$', views.movie_view, name='movie_view'),  # TODO: Update this
    url(r'^$', views.user_view, name='user_view'),  # TODO: Update this
]

# For reference from: https://docs.djangoproject.com/en/1.10/intro/tutorial03/
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
