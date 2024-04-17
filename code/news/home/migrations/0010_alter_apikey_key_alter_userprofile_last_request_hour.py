# Generated by Django 5.0.4 on 2024-04-17 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_userprofile_last_request_hour_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_request_hour',
            field=models.IntegerField(default=21),
        ),
    ]