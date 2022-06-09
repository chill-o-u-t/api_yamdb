# Generated by Django 2.2.16 on 2022-06-09 14:29

from django.db import migrations, models
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20220609_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(validators=[reviews.models.ValidateYear.validate_year], verbose_name='Год выхода'),
        ),
    ]
