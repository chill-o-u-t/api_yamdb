from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import serializers

from reviews.models import Comment, Review, Title
from core.models import User
from .tokens import account_activation_token


class AuthSerializer(serializers.ModelSerializer):
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

    def validate_score(self, data):
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
