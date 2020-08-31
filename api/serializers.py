from rest_framework import serializers

from .models import Genre, Category, Title, GenreTitle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'genre_id', 'title_id')
        model = GenreTitle


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreTitleSerializer(many=True, read_only=True)
    category = CategorySerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
