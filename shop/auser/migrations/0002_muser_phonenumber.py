# Generated by Django 3.2.9 on 2021-12-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='muser',
            name='phonenumber',
            field=models.PositiveIntegerField(blank=True, max_length=11, null=True),
        ),
    ]
