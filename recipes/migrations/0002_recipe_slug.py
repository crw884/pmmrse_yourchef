# Generated by Django 4.2.20 on 2025-05-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(default=None, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
