# Generated by Django 4.1.7 on 2023-04-03 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_book_authors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='books',
            field=models.ManyToManyField(related_name='stores', to='catalog.book'),
        ),
    ]