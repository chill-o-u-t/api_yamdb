import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from api.validators import validate_year


class UsernameValidateMixin:

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('restricted or invalid name')
        if not re.match(r'[\w.@+-@./+-]+', value):
            raise ValidationError('restricted symbols in username')
        return value


class User(AbstractUser, UsernameValidateMixin):
    ADMIN = 'admin'
    MODERATOR = "moderator"
    USER = "user"

    ROLES = ((ADMIN, 'admin'), (MODERATOR, 'moderator'), (USER, 'user'))
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(
        unique=True,
    )
    confirmation_code = models.CharField(
        'confirmation code',
        max_length=6,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField("Путь", max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField("Путь", max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField('Название', max_length=150)
    year = models.IntegerField('Год выхода', validators=[validate_year])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='genres',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='categorys',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='review_authors'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    text = models.TextField(
        'Текст',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_title_author"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comment_authors'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    text = models.TextField(
        'Текст',
    )
