from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    class UserRole(models.TextChoices):
        admin = 'admin'
        moderator = 'moderator'
        user = 'user'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.user)
    bio = models.TextField(max_length=500, blank=True, null=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)

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
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='titles')


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
