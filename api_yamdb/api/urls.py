from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import ReviewViewSet, CommentViewSet, AuthViewSet


router_v1 = SimpleRouter()
router_v1.register('rewiews', ReviewViewSet, basename='rewiews')
router_v1.register('comments', CommentViewSet, basename='comments')
router_v1.register('auth/signup', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router_v1.urls)),
]
