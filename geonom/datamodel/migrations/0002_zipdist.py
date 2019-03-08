# Generated by Django 2.1.7 on 2019-03-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZipDist',
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
