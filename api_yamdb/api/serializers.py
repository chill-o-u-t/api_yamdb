from django.core.validators import MaxValueValidator, RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Comment,
    Review,
    Genre,
    Category,
    Title,
    User,
    UsernameValidateMixin,
)
from reviews.utils import get_year


class AuthSerializer(serializers.Serializer, UsernameValidateMixin):
    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(max_length=254)


class TokenSerializer(serializers.Serializer, UsernameValidateMixin):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=6)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    author=self.context['request'].user,
                    title=self.context['view'].kwargs.get('title_id')
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение!'
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
    year = serializers.IntegerField(
        validators=(MaxValueValidator(
            get_year,
            message='Нельзя добавлять произведения из будущего!'),
        )
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title


class TitleGetSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()
    read_only_fields = '__all__'

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


class UserSerializer(serializers.ModelSerializer, UsernameValidateMixin):
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
