# Generated by Django 3.2.9 on 2021-12-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0002_auto_20211229_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='number',
            field=models.PositiveIntegerField(),
        ),
    ]
