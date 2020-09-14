from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='author.username')
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        title = get_object_or_404(
            Title, pk=self.context['view'].kwargs['title_id']
        )
        review_is = title.review.filter(author=self.context['request'].user)
        if review_is.exists():
            raise ValidationError('Отзыв уже есть!')
        return data


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenGainSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.FloatField(
        source='review__score__avg', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(), required=True)
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), required=True,
        many=True)

    class Meta:
        fields = '__all__'
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only='True',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'review_id', 'text', 'pub_date')
        model = Comment
