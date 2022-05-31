from rest_framework.routers import SimpleRouter
from django.urls import path, include

from api.views import GenreViewSet, CategoryViewSet, TitleViewSet


router = SimpleRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
]
