# Generated by Django 2.1.7 on 2019-04-03 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20190402_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='root',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='search.Website'),
        ),
    ]
