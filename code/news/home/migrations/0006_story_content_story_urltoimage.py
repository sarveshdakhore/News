# Generated by Django 5.0.4 on 2024-04-11 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_story_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='story',
            name='urlToImage',
            field=models.URLField(default=''),
        ),
    ]
