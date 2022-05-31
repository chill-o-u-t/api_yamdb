from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime


from reviews.models import Genre, Category, Title, GenreTitle


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
