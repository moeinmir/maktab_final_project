# Generated by Django 3.2.9 on 2022-01-06 19:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0017_basketsearch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketsearch',
            name='begin_date',
            field=models.DateField(default=datetime.date(1500, 10, 10)),
        ),
        migrations.AlterField(
            model_name='basketsearch',
            name='end_date',
            field=models.DateField(default=datetime.date(2500, 10, 10)),
        ),
    ]
