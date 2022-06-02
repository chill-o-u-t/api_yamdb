from requests import Response
from rest_framework import viewsets
# from .permissions import IsAdminOrReadOnly
from .tokens import account_activation_token
from reviews.models import User
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view

from reviews.models import Genre, Category, Title
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitleSerializer,
    UserSerializer
)


class AuthViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def signup(request):
    user = User.objects.create(
        username=request.data.get('username'),
        email=request.data.get('email'),
        password=''
    )
    mail_subject = 'Activate your account.'
    message = f'{account_activation_token.make_token(user)}'
    print('------------------------')
    print(message)
    to_email = request.data.get('email')
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    # email.send()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
