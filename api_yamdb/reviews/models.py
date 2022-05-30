from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    # отнаследовать
    name = models.CharField('Жанр', max_length=150, unique=True)
    slug = models.SlugField('Путь', max_length=150, unique=True)


class Category(models.Model):
    # отнаследовать
    name = models.CharField('Категория', max_length=150, unique=True)
    slug = models.SlugField('Путь', max_length=150, unique=True)


class Title(models.Model):
    # field rating - ?

    name = models.CharField('Название', max_length=150)
    year = models.DateField('Год выхода')
    description = models.TextField('Описание')
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='category'
    )


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
