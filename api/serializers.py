from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import Category, Genre, Title
User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, read_only=True)
    genre = GenreSerializer(required=False, many=True, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def get_objects_by_slug(self, validated_data):
        if self.initial_data.get('category'):
            category_slug = self.initial_data.get('category')
            category = get_object_or_404(Category, slug=category_slug)
            validated_data['category'] = category

        if self.initial_data.get('genre'):
            genres = []
            for slug in self.initial_data.getlist('genre'):
                genre = get_object_or_404(Genre, slug=slug)
                genres.append(genre)
            validated_data['genre'] = genres

        return validated_data

    def create(self, validated_data):
        validated_data = self.get_objects_by_slug(validated_data)

        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data = self.get_objects_by_slug(validated_data)

        instance = super().update(instance, validated_data)
        return instance


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenGainSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role',)
        model = User
