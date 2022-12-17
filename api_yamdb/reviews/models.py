from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    role = models.CharField(
        verbose_name='Уровень доступа',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            ),
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_superuser or self.role == "Administrator"

    @property
    def is_moder(self):
        return self.role == 'Moderator'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='название произведения')
    year = models.IntegerField(
        verbose_name='Год выхода в свет',
        default=0,
        db_index=True
    )
    description = models.CharField(blank=True, null=True, max_length=256)
    category = models.ForeignKey(
        Category,
        default='-',
        on_delete=models.SET_DEFAULT,
        related_name='titles',
        verbose_name='категория',
    )
    genre = models.ManyToManyField(
        Genre,
        default='-',
        related_name='titles',
        verbose_name='категория',
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        db_column='genre_id'
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_column='title_id'
    )

    def __str__(self):
        return f'{self.genre_id} {self.title_id}'
