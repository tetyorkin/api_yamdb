from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404

from .models import Category, Genre, Title, User, Review, Comment
from django.db.models import Avg


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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category', 'rating')
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

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
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )
        model = User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        exclude =['title',]
        #fields = '__all__'
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset = Review.objects.all(),
        #         fields=['author', 'title']
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #title = serializers.SlugRelatedField(slug_field='name', queryset=Title.objects.all())
    #review = serializers.SlugRelatedField(slug_field='text', queryset=Review.objects.all())
    
    class Meta:
        fields = '__all__'
        model = Comment