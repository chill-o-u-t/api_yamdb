from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from core.models import SortModel, EntryModel


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = "moderator"
    USER = "user"

    ROLES = ((ADMIN, 'admin'), (MODERATOR, 'moderator'), (USER, 'user'))
    role = models.CharField(
        max_length=1,
        choices=ROLES,
        default='user'
    )
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(
        unique=True,
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


class Genre(SortModel):
    pass


class Category(SortModel):
    pass


class Title(models.Model):
    name = models.CharField('Название', max_length=150)
    year = models.IntegerField('Год выхода')
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='genre',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='category',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(EntryModel):
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='review_author'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_title_author"
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(EntryModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comment'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comment_author'
    )