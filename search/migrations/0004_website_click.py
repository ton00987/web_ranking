# Generated by Django 2.1.7 on 2019-04-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20190403_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='click',
            field=models.IntegerField(default=0),
        ),
    ]