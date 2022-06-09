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
    ValidateYear
)


class AuthSerializer(serializers.Serializer, UsernameValidateMixin):
    username = serializers.CharField(max_length=150)
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


class TitlePostSerializer(ValidateYear, serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(), many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()
    read_only_fields = ('id', 'name', 'year', 'rating', 'description',
                        'category', 'genre')

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
