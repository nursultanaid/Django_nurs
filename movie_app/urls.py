from django.contrib import admin
from django.urls import path, include
from movie_app.views import DirectorListAPIView, DirectorDetailAPIView, MovieListAPIView, MovieDetailAPIView, \
    ReviewListAPIView, ReviewDetailAPIView

urlpatterns = [
    path('directors/', DirectorListAPIView.as_view()),
    path('directors/<int:id>/', DirectorDetailAPIView.as_view()),
    path('movies/', MovieListAPIView.as_view()),
    path('movies/<int:id>/', MovieDetailAPIView.as_view()),
    path('reviews/', ReviewListAPIView.as_view()),
    path('reviews/<int:id>/', ReviewDetailAPIView.as_view())

]