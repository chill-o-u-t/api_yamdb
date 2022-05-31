from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly
from reviews.models import Genre, Category
from .serializers import GenreSerializer, CategorySerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer