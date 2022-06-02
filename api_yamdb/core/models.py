from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('a', 'Administrator'),
        ('m', 'Moderator'),
        ('u', 'User'),
    )
    role = models.CharField(
        max_length=1, choices=ROLES, default='u'
    )


class SortModel(models.Model):
    """Абстрактная модель."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField("Путь", max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class EntryModel(models.Model):
    """Абстрактная модель."""
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
        related_name='author'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True
