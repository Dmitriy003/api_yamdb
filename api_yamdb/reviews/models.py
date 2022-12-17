from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
