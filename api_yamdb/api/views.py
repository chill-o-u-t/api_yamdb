from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Review,
    Comment,
    Title,
    Genre,
    Category,
    User,
    UserConfirmation
)
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    AuthSerializer,
)
from .tokens import get_tokens_for_user
from .permissions import (
    IsSuperUserOrReadOnly,
    AuthorOrStaffPermission,
    AdminPermission
)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    print(request.data)
    for field in ('username', 'confirmation_code'):
        if not request.data.get(field):
            return Response(
                {f'{field}': 'Это обязательное поле'},
                status=status.HTTP_400_BAD_REQUEST
            )
    user = UserConfirmation.objects.get(
        user__username=request.data.get('username'),
        confirmation_code=request.data.get('confirmation_code')
    )
    if user:
        tokens = get_tokens_for_user(user.user)
        user.delete()
        return Response(
            tokens,
            status=status.HTTP_200_OK
        )
    return Response(
        {'Пользователь не запрашивал код'},
        status=status.HTTP_404_NOT_FOUND
    )


class AuthViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = AuthSerializer


'''
class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
'''


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
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


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminPermission,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffPermission,)

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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TitlePostSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
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