# Generated by Django 2.1.7 on 2019-03-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0003_zipdist_2digits'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZipDist_grid_10',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_lat', models.IntegerField()),
                ('a_lon', models.IntegerField()),
                ('b_lat', models.IntegerField()),
                ('b_lon', models.IntegerField()),
                ('distance_fly', models.FloatField()),
                ('distance_route', models.FloatField()),
            ],
        ),
    ]
