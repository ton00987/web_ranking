# Generated by Django 2.1.7 on 2019-04-23 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0004_website_click'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WordWebsite',
            new_name='Have',
        ),
        migrations.RemoveField(
            model_name='website',
            name='root',
        ),
        migrations.AddField(
            model_name='website',
            name='website1',
            field=models.ManyToManyField(default=None, null=True, to='search.Website'),
        ),
    ]
