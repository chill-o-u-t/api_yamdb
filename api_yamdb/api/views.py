from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.crypto import get_random_string
from rest_framework.decorators import (
    api_view,
    permission_classes,
    action
)
from rest_framework import status, mixins
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from reviews.models import (
    Review,
    Title,
    Genre,
    Category,
    User,
)
from .send_mail import send_mail
from .filters import FilterForTitle
from .tokens import get_tokens_for_user
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    AuthSerializer,
    UserSerializer,
    TokenSerializer
)
from .permissions import (
    ReadOrAuthorAndStaff,
    Admin,
    AdminOrReadOnly
)


class ListDestroyCreateGenreCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def signup(request):
    serializer = AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
        )
    except IntegrityError:
        return Response(
            {'username does not match email'},
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = get_random_string(length=6)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(user.email, user.confirmation_code)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if (
        user.confirmation_code
        != serializer.validated_data.get('confirmation_code')
    ):
        return Response(
            {'invalid confirmation code'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = ''
    user.save()
    tokens = get_tokens_for_user(user)
    return Response(
        tokens,
        status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (Admin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'

    @action(methods=['patch', 'get'],
            detail=False,
            permission_classes=[IsAuthenticated],
            url_path='me',
            url_name='me'
            )
    def me(self, request):
        if self.request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = UserSerializer(request.user, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        ReadOrAuthorAndStaff,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        ReadOrAuthorAndStaff,
        IsAuthenticatedOrReadOnly
    )

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id', 'title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class GenreViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListDestroyCreateGenreCategoryViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    serializer_class = TitlePostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle
    ordering_fields = ('name',)
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitlePostSerializer
