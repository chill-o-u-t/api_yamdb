import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from .utils import get_year


class UsernameValidateMixin:
    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('ограниченное или недопустимое имя пользователя')
        if not re.match(r'[\w.@+-@./+-]+', value):
            raise ValidationError('ограниченные символы в имени пользователя')
        return value


class User(AbstractUser, UsernameValidateMixin):
    ADMIN = 'admin'
    MODERATOR = "moderator"
    USER = "user"

    ROLES = ((ADMIN, 'admin'), (MODERATOR, 'moderator'), (USER, 'user'))
    role = models.CharField(
        max_length=len(max(ROLES)),
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=150,
    )
    first_name = models.TextField(
        blank=True,
        null=True,
        max_length=150,
    )
    last_name = models.TextField(
        blank=True,
        null=True,
        max_length=150,
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
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
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class SortModel(models.Model):
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField("Путь", max_length=50, unique=True)

    class Meta:
        ordering = ('-name',)
        abstract = True


class EntryModel(models.Model):
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )
    text = models.TextField(
        'Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='%(class)s'
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Genre(SortModel):
    pass


class Category(SortModel):
    pass


class Title(models.Model):
    name = models.TextField('Название')
    year = models.IntegerField(
        'Год выхода',
        validators=[MaxValueValidator(get_year())]
    )
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

    class Meta:
        ordering = ('-year',)


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(EntryModel):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta(EntryModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_title_author"
            )
        ]


class Comment(EntryModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )

