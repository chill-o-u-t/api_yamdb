from rest_framework.routers import SimpleRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include

<<<<<<< HEAD
from .views import GenreViewSet, CategoryViewSet, TitleViewSet, AuthViewSet
from .views import signup

router_v1 = SimpleRouter()
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
=======
from .views import ReviewViewSet, CommentViewSet, AuthViewSet


router_v1 = SimpleRouter()
router_v1.register('rewiews', ReviewViewSet, basename='rewiews')
router_v1.register('comments', CommentViewSet, basename='comments')
>>>>>>> submaster
router_v1.register('auth/signup', AuthViewSet, basename='auth')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
<<<<<<< HEAD
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
=======
>>>>>>> submaster
]
