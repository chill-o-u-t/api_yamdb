from reviews.models import Category, Genre, GenreTitle
from reviews.models import Title, Comment, Review, User
import csv


def run():
    Comment.objects.all().delete()
    Review.objects.all().delete()
    Title.objects.all().delete()
    Category.objects.all().delete()
    Genre.objects.all().delete()
    GenreTitle.objects.all().delete()
    User.objects.all().delete()
    with open('static/data/users.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            user, _ = User.objects.get_or_create(**dict_of_data)
            user.save()

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
            dict_of_data["title"] = Title.objects.get(
                id=dict_of_data["title_id"])
            dict_of_data["author"] = User.objects.get(
                id=dict_of_data["author"])
            object, _ = Review.objects.get_or_create(**dict_of_data)
            object.save()

    with open('static/data/comments.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            zip_obj = zip(headers, row)
            dict_of_data = dict(zip_obj)
            dict_of_data["review"] = Review.objects.get(
                id=dict_of_data["review_id"])
            dict_of_data["author"] = User.objects.get(
                id=dict_of_data["author"])
            object, _ = Comment.objects.get_or_create(**dict_of_data)
            object.save()
