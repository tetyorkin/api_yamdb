from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    class UserRole(models.TextChoices):
        admin = 'admin'
        moderator = 'moderator'
        user = 'user'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=10, choices=UserRole.choices, default=UserRole.user
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == User.UserRole.admin or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.UserRole.moderator


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(
        blank=True, null=True, db_index=True
    )
    description = models.CharField(max_length=100, blank=True, null=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review'
    )
    score = models.PositiveIntegerField(
        null=False,
        default=5,
        validators=(
            MinValueValidator(1), MaxValueValidator(10)
        )
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comment'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
