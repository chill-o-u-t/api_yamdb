# Generated by Django 2.2.16 on 2022-06-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('a', 'Administrator'), ('m', 'Moderator'), ('u', 'User')], default='u', max_length=1),
        ),
    ]