from rest_framework import serializers

from .models import Category, Genre, Title, User


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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenGainSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role', )
        model = User
