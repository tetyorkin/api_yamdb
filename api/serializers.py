from rest_framework import serializers

from .models import Genre, Category, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'category', 'genre', 'name', 'year')
        model = Title
