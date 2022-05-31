from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import ReviewViewSet


router_v1 = SimpleRouter()
router_v1.register('rewiews', ReviewViewSet, basename='rewiews')

urlpatterns = [
    path('', include(router.urls)),
]
