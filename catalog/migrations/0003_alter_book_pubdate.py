# Generated by Django 4.1.7 on 2023-03-31 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pubdate',
            field=models.FloatField(),
        ),
    ]
