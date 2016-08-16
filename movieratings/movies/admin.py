from django.contrib import admin

from .models import Rater, Rating, Movie


admin.site.register(Rater)
admin.site.register(Rating)
admin.site.register(Movie)
