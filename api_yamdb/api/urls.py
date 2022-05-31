from rest_framework.routers import SimpleRouter
from django.urls import path, include

from api.views import GenreViewSet, CategoryViewSet


router = SimpleRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
]