from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

app_name = 'movies'

urlpatterns = [
    url(r'^$', cache_page(60 * 15)(views.index), name='index'),
    url(r'^movie/$', views.movie_view, name='movie_view'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$',
        views.movie_detail, name='movie_detail'),
    url(r'^rater/$', views.user_view, name='user_view'),
    url(r'^rater/(?P<rater_id>[0-9]+)/$',
        views.user_detail, name='user_detail'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^test/$', views.test_table, name='test_table'),
    url(r'^movies_for_you/$', views.movies_for_you, name='movies_for_you'),
]


# For reference from: https://docs.djangoproject.com/en/1.10/intro/tutorial03/
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
# ]
