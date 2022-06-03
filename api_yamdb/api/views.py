from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.permissions import  IsAuthenticated


from reviews.models import Review, Comment, Title, Genre, Category, User, UserConfirmation
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)
from .permissions import (
    AuthorOrStaffPermission,
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated, AuthorOrStaffPermission)
    filter_backends = (filters.SearchFilter,)

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('titles_id')
        )

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            user=self.request.user
        )

    def get_raiting(self):
        reviews = self.get_title().reviews
        summ_of_scores = 0
        for review in reviews:
            summ_of_scores += review.score
        return summ_of_scores / reviews.count()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffPermission, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)

    def get_review(self):
        return get_object_or_404(
            Review, title=self.kwargs.get('title')
        )

    def get_queryset(self):
        return self.get_review().comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

