from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime


from reviews.models import Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(), many=True)
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())

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
