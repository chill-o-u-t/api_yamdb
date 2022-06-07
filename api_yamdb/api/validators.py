from django.core.exceptions import ValidationError
import datetime


def validate_year(data):
    year_now = datetime.datetime.now().year
    if data:
        if data > year_now:
            raise ValidationError({
                'year': "You can't add titles that are not release yet",
            })
