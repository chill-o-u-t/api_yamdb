import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Comment,
    Review,
    Genre,
    Category,
    Title,
    User,
)
from .tokens import account_activation_token


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
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                author=self.context['request'].user,
                title=get_object_or_404(
                    Title,
                    pk=self.context['view'].kwargs.get('titles_id')
                )
            ).exists():
                raise serializers.ValidationError(
                    'Нельзя повторно писать ревью'
                )
        return super().validate(data)

    class Meta:
        model = Review
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
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
