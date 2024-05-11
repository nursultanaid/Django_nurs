from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import status
from .models import Director, Movie, Review
from .serializers import  (DirectorSerializer, MovieSerializer, ReviewSerializer,
                           MovieValiditySerializer, DirectorValiditySerializer, ReviewValiditySerializer)


class DirectorListAPIView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def post(self, request, *args, **kwargs):
        validator = DirectorValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        name = validator.validated_data['name']
        Director.objects.create(name=name)
        return Response(validator.errors, status=status.HTTP_201_CREATED)


class DirectorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        director_detail = self.get_object()
        serializer = DirectorValiditySerializer(director_detail, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        director_detail.name = serializer.validated_data['name']
        director_detail.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


    def post(self, request, *args, **kwargs):
        validator = MovieValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': validator.errors})
        title = request.data['title']
        director_id = request.data['director']
        description = request.data['description']
        duration = request.data['duration']
        Movie.objects.create(title=title, director_id=director_id, description=description, duration=duration)
        return Response(status=status.HTTP_201_CREATED)


class MovieDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


    def put(self, request, *args, **kwargs):
        movie_detail = self.get_object()
        validator = MovieValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        movie_detail.title = validator.validated_data['title']
        movie_detail.director_id = validator.validated_data['director']
        movie_detail.description = validator.validated_data['description']
        movie_detail.duration = validator.validated_data['duration']
        movie_detail.save()
        return Response(status=status.HTTP_201_CREATED)


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def post(self, request, *args, **kwargs):
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        text = validator.validated_data['text']
        movie_id = validator.validated_data['movie']
        stars = validator.validated_data['stars']
        Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        return Response(status=status.HTTP_201_CREATED)



class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        review_detail = self.get_object()
        validator = ReviewValiditySerializer(data=request.data)
        if not validator.is_valid():
            return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        review_detail.text = validator.validated_data['text']
        review_detail.movie_id = validator.validated_data['movie']
        review_detail.stars = validator.validated_data['stars']
        review_detail.save()
        return Response(status=status.HTTP_201_CREATED)