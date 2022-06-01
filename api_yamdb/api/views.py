from rest_framework import viewsets, filters
from rest_framework.response import Response
from django.forms.models import model_to_dict

from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, CategorySerializer
from .serializers import TitleGetSerializer, TitlePostSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitlePostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitlePostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serialized_data = serializer.data
        category_dict = model_to_dict(
            Category.objects.get(slug=serialized_data['category'])
        )
        category_dict.pop('id')
        serialized_data['category'] = category_dict

        genres = list()
        for genre in serialized_data['genre']:
            genre_dict = model_to_dict(
                Genre.objects.get(slug=genre)
            )
            genre_dict.pop('id')
            genres.append(genre_dict)
        serialized_data['genre'] = genres

        return Response(serialized_data)

    def update(self, request, pk, partial=False):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serialized_data = serializer.data
        category_dict = model_to_dict(
            Category.objects.get(slug=serialized_data['category'])
        )
        category_dict.pop('id')
        serialized_data['category'] = category_dict
        genres = list()
        for genre in serialized_data['genre']:
            genre_dict = model_to_dict(
                Genre.objects.get(slug=genre)
            )
            genre_dict.pop('id')
            genres.append(genre_dict)
        serialized_data['genre'] = genres

        return Response(serialized_data)
