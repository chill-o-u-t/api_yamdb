from rest_framework import viewsets

from reviews.models import Review, Comment


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass