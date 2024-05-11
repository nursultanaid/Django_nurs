from rest_framework import serializers
from .models import Director, Movie, Review

class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id name'.split()

class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director created_at updated_at'.split()

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
class DirectorSerializer(serializers.ModelSerializer):
    director_movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['id', 'name', 'director_movies_count']

    def get_director_movies_count(self, obj):
        count = obj.movies.count()
        return count


class DirectorValiditySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=2)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie'.split()
        fields = ['id', 'text', 'movie', 'stars']

class ReviewValiditySerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2, max_length=100)
    movie = serializers.IntegerField(min_value=1)
    stars = serializers.IntegerField(min_value=1, max_value=5)

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, required=False)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews average_rating created_at updated_at'.split()

    def get_average_rating(self, movie):
        reviews = movie.reviews.all()
        if reviews:
            sum_reviews = sum(i.stars for i in reviews)
            average = sum_reviews/len(reviews)
            return average
        return None

class MovieValiditySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=2)
    description = serializers.CharField(max_length=500, min_length=1)
    duration = serializers.CharField(max_length=100, min_length=1)
    director = serializers.IntegerField(min_value=1)
