from rest_framework import serializers

from .models import Category, Genre, Title, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TitleSerializer, self).__init__(*args, **kwargs)
        if 'view' in self.context and self.context['view'].action != 'create':
            self.fields.update({"category": CategorySerializer(), "genre": GenreSerializer(many=True)})

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        depth = 1


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
    author = serializers.ReadOnlyField(source='author.username')
    title = serializers.SlugRelatedField(slug_field='name', queryset=Title.objects.all())

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #title = serializers.SlugRelatedField(slug_field='name', queryset=Title.objects.all())
    review = serializers.SlugRelatedField(slug_field='text', queryset=Review.objects.all())
    
    class Meta:
        fields = '__all__'
        model = Comment