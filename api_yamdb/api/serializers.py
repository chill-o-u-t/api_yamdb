import datetime

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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = SlugRelatedField(slug_field='slug', read_only=True)

    def validate(self, data):
        year_now = datetime.datetime.now().year
        if "year" in data:
            if data["year"] > year_now:
                raise serializers.ValidationError({
                    "year": "You can't add titles that are not release yet",
                })

        return super(TitleSerializer, self).validate(data)

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get(
                **genre)
            GenreTitle.objects.create(
                achievement=current_genre, title=title)
        return title

    class Meta:
        fields = ('name', 'year', 'description', 'genre', 'category')
        model = Title
