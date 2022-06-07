from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
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

from core.send_mail import send_mail
from .filters import FilterForTitle
from core.tokens import get_tokens_for_user, account_activation_token
from reviews.models import (
    Review,
    Title,
    Genre,
    Category,
    User,
)
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
    AuthorOrStaffPermission,
    AdminPermission,
    AdminOrReadOnlyPermission
)


class ListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


@api_view(['POST'])
@permission_classes((AllowAny, ))
def signup(request):
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        user, _ = User.objects.get_or_create(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'),
        )
        confirmation_code = f'{account_activation_token.make_token(user)}'
        send_mail(user.email, confirmation_code)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    print(request.data)
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        tokens = get_tokens_for_user(user)
        return Response(
            tokens,
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AdminPermission,)
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
        instance = get_object_or_404(User, username=request.user.username)
        if self.request.method == 'PATCH':
            serializer = UserSerializer(
                instance,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save(role=instance.role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(instance, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorOrStaffPermission,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().review.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorOrStaffPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_review(self):
        return get_object_or_404(
            Review, id=self.kwargs.get('review_id', 'title_id')
        )

    def get_queryset(self):
        return self.get_review().comment.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class GenreViewSet(ListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(ListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('review__score'))
    permission_classes = (AdminOrReadOnlyPermission,)
    serializer_class = TitlePostSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle
    ordering_fields = ('name',)
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitlePostSerializer
