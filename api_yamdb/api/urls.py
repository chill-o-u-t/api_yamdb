from rest_framework.routers import SimpleRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include

from .views import (
    ReviewViewSet,
    CommentViewSet,
    AuthViewSet,
    GenreViewSet,
    TitleViewSet,
    CategoryViewSet
)


router_v1 = SimpleRouter()
router_v1.register('rewiews', ReviewViewSet, basename='rewiews')
router_v1.register('comments', CommentViewSet, basename='comments')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('auth/signup', AuthViewSet, basename='auth')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
