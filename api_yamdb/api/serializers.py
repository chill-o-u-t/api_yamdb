import datetime

<<<<<<< HEAD
from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import User

from reviews.models import Genre, Category, Title, GenreTitle
from .tokens import account_activation_token


class UserSerializer(serializers.ModelSerializer):
    password = ''

    def validate(self, data):
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
        message = f'{account_activation_token.make_token(user)}'
        print('--confirmation_code--')
        print(message)
        to_email = validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        # email.send()
        return user

    class Meta:
        model = User
        fields = ('username', 'email')
=======
# from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Genre, Category, Title, User
from .tokens import account_activation_token
>>>>>>> submaster


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
        # mail_subject = 'Activate your account.'
        message = f'{account_activation_token.make_token(user)}'
        print('--confirmation_code--')
        print(message)
        # to_email = validated_data.get('email')
        # email = EmailMessage(
        #     mail_subject, message, to=[to_email]
        # )
        # email.send()
        return user

    class Meta:
        model = User
        fields = ('username', 'email')


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
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


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

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def validate(self, data):
        year_now = datetime.datetime.now().year
        if "year" in data:
            if data["year"] > year_now:
                raise serializers.ValidationError({
                    "year": "You can't add titles that are not release yet",
                })
        return super(TitlePostSerializer, self).validate(data)


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
