# Generated by Django 2.1.7 on 2019-03-28 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0004_zipdist_grid_10'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zipcode',
            name='zip_code',
            field=models.CharField(max_length=30),
        ),
    ]