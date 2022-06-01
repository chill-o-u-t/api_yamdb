from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import ReviewViewSet, CommentViewSet


router_v1 = SimpleRouter()
router_v1.register('rewiews', ReviewViewSet, basename='rewiews')
router_v1.register('comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router_v1.urls)),
]
