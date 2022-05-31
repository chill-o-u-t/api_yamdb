from django.db import models
from reviews.models import Me


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
        Me,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comment_author'
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True
