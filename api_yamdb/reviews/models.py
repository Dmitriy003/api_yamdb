from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


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
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )
    genre = models.ForeignKey(
        'GenreTitle',
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    ''' Модель отзыва на произведение.'''
    title = models.ForeignKey(Title,
        on_delete=models.CASCADE,
        related_name='title',
        verbose_name='Заголовок отзыва',
        )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='review_author',
        verbose_name='Автор')
    score = models.PositiveSmallIntegerField(verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='comment_author',
        verbose_name='Автор комментария',)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text
