# Generated by Django 2.1.7 on 2019-06-15 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NewsSite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='content',
            field=models.TextField(default=''),
        ),
    ]
