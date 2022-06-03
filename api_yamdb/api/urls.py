from rest_framework.routers import SimpleRouter
from django.urls import path, include

from .views import ReviewViewSet, CommentViewSet, AuthViewSet, get_token

router_v1 = SimpleRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='rewiews'
)
router_v1.register(
    r'reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('auth/signup', AuthViewSet, basename='auth')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', get_token),

]
