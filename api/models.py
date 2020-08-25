from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class UserRole(models.TextChoices):
        admin = 'admin'
        moderator = 'moderator'
        user = 'user'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.user)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='titles')


class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
