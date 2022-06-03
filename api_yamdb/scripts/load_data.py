from reviews.models import Category, Genre, GenreTitle, Title, Comment, Review
import csv


def run():
    Title.objects.all().delete()
    Category.objects.all().delete()
    Genre.objects.all().delete()
    GenreTitle.objects.all().delete()
    Comment.objects.all().delete()
    Review.objects.all().delete()
    with open('static/data/category.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            category, _ = Category.objects.get_or_create(**dict_of_data)
            category.save()

    with open('static/data/genre.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            genre, _ = Genre.objects.get_or_create(**dict_of_data)
            genre.save()

    with open('static/data/titles.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            dict_of_data["category"] = Category.objects.get(
                id=dict_of_data["category"])
            title, _ = Title.objects.get_or_create(**dict_of_data)
            title.save()

    with open('static/data/genre_title.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            object, _ = GenreTitle.objects.get_or_create(**dict_of_data)
            object.save()

    with open('static/data/review.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            dict_of_data["title"] = Review.objects.get(
                id=dict_of_data["title"])
            object, _ = Review.objects.get_or_create(**dict_of_data)
            object.save()

    with open('static/data/comments.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            dict_of_data["review"] = Review.objects.get(
                id=dict_of_data["review"])
            object, _ = Comment.objects.get_or_create(**dict_of_data)
            object.save()

