#  from django.contrib.auth import get_user_model
from django.db import models


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
