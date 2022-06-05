from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from core.send_mail import send_mail
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
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminPermission,
        AuthorOrStaffPermission,
        IsAuthenticatedOrReadOnly
    )

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('titles_id')
        )

    def get_queryset(self):
        return self.get_title().review

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            user=self.request.user
        )

    def get_raiting(self):
        reviews = self.get_title().review
        summ_of_scores = 0
        for review in reviews:
            summ_of_scores += review.score
        return summ_of_scores / reviews.count()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorOrStaffPermission,
        IsAuthenticated
    )
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review, title=self.kwargs.get('title')
        )

    def get_queryset(self):
        return self.get_review().comment

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    serializer_class = TitlePostSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleGetSerializer
        return TitlePostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serialized_data = serializer.data
        category_dict = model_to_dict(
            Category.objects.get(slug=serialized_data['category'])
        )
        category_dict.pop('id')
        serialized_data['category'] = category_dict

        genres = list()
        for genre in serialized_data['genre']:
            genre_dict = model_to_dict(
                Genre.objects.get(slug=genre)
            )
            genre_dict.pop('id')
            genres.append(genre_dict)
        serialized_data['genre'] = genres

        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, partial=False):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serialized_data = serializer.data
        category_dict = model_to_dict(
            Category.objects.get(slug=serialized_data['category'])
        )
        category_dict.pop('id')
        serialized_data['category'] = category_dict
        genres = list()
        for genre in serialized_data['genre']:
            genre_dict = model_to_dict(
                Genre.objects.get(slug=genre)
            )
            genre_dict.pop('id')
            genres.append(genre_dict)
        serialized_data['genre'] = genres

        return Response(serialized_data)