# Generated by Django 4.2.2 on 2023-07-04 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_authors', '0003_alter_authors_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='authors',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
