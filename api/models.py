from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)


class Title(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True related_name='titles')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True related_name='titles')
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
