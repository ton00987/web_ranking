# Generated by Django 2.1.7 on 2019-04-28 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0005_date_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
