# Generated by Django 2.1.7 on 2019-04-29 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_title_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='ref',
            field=models.ManyToManyField(default=None, null=True, to='search.Website'),
        ),
        migrations.AlterField(
            model_name='website',
            name='url',
            field=models.CharField(db_index=True, max_length=10000),
        ),
    ]
