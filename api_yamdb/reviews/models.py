from django.db import models
from core.models import SortModel
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('a', 'Administrator'),
        ('m', 'Moderator'),
        ('u', 'User'),
    )
    role = models.CharField(
        max_length=1, choices=ROLES, default='u')


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
        blank=True,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.PROTECT,
        related_name='category',
        blank=True,
        null=True,
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    # field score - ?
    # score = models.???
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='review'
    )

    # отнаследовать
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
        related_name='review_author'
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='review'
    )

    # отнаследовать
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
        related_name='comment_author'
    )
