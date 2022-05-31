from django.db import models


class SortModel(models.Model):
    """Абстрактная модель."""
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField("Путь",max_length=50, unique=True)
    
    def __str__(self):
        return f'{self.name}'
        
    class Meta:
        abstract = True
