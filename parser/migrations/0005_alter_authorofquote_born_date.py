# Generated by Django 4.1.7 on 2023-04-13 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser', '0004_alter_authorofquote_born_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorofquote',
            name='born_date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
