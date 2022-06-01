from django.contrib.auth import get_user_model
from django.db import models

from core.models import SortModel, EntryModel

Me = get_user_model()


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


class Review(EntryModel):
    score = models.IntegerField(choices=(range(1, 11)))
    title = models.ForeignKey(
        Title,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='review'
    )


class Comment(EntryModel):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='review'
    )
