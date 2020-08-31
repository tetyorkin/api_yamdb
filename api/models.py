from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='titles')


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='genre')
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='title')

    class Meta:
        unique_together = ('title_id', 'genre_id')
