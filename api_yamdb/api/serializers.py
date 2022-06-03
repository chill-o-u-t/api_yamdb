from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Review, Genre, Category, Title, User, UserConfirmation


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
