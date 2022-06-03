import datetime

from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import (
    Comment,
    Review,
    Genre,
    Category,
    Title,
    User,
    UserConfirmation
)
from .tokens import account_activation_token


class AuthSerializer(serializers.ModelSerializer):
    password = ''

    def validate(self, data):
        print(data)
        if data['username'] == 'me':
            raise serializers.ValidationError({
                "username": "This username is restricted",
            })
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=self.password
        )
        mail_subject = 'Activate your account.'
        confirmation_code = f'{account_activation_token.make_token(user)}'
        print('--confirmation_code--')
        print(confirmation_code)
        to_email = validated_data.get('email')
        email = EmailMessage(
            mail_subject, confirmation_code, to=[to_email]
        )
        email.send()
        UserConfirmation.objects.create(
            user=user,
            confirmation_code=confirmation_code
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email')


'''
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    password = ''

    def validate(self, data):
        data = super().validate(data)
        if UserConfirmation.get(user=data.user).exists():
            print(data.user)
        data['password'] = ''
        print(data)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['confirmation_code'] = ''
        token['password'] = ''
        return token
'''


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.object.filter(
                author=self.context['request'].user,
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs.get('titles_id')
                )
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя повторно писать ревью'
                )
        return data

    class Meta:
        model = Review
        fields = ('__all__',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


class TitlePostSerializer(serializers.ModelSerializer):
  
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    
    def validate(self, data):
        print(data)
        year_now = datetime.datetime.now().year
        if "year" in data:
            if data["year"] > year_now:
                raise serializers.ValidationError({
                    "year": "You can't add titles that are not release yet",
                })
        return super(TitlePostSerializer, self).validate(data)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
