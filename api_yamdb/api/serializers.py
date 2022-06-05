import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from core.tokens import account_activation_token
from reviews.models import (
    Comment,
    Review,
    Genre,
    Category,
    Title,
    User,
)


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError('restricted name')
        if (
                User.objects.filter(email=attrs.get('email')).exists()
                or User.objects.filter(username=attrs.get('username')).exists()
        ):
            raise serializers.ValidationError('duplicated mail')
        return super().validate(attrs)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        if not account_activation_token.check_token(
            get_object_or_404(
                User,
                username=attrs.get('username')
            ),
            attrs.get('confirmation_code')
        ):
            raise serializers.ValidationError('Invalid token')
        return super().validate(attrs)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        is_exist = Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id'),
        ).exists()
        if is_exist and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Пользователь уже оставлял отзыв на это произведение'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'pub_date', 'score')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitlePostSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    def validate(self, data):
        year_now = datetime.datetime.now().year
        if 'year' in data:
            if data['year'] > year_now:
                raise serializers.ValidationError({
                    'year': "You can't add titles that are not release yet",
                })
        return super(TitlePostSerializer, self).validate(data)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )
        model = Title
        read_only_fields = ('id', 'rating')


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'category',
            'genre'
        )
        model = Title


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )

    class Meta:
        fields = (
            'username',
            'bio',
            'email',
            'role',
            'first_name',
            'last_name',
        )
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email']
            )
        ]
