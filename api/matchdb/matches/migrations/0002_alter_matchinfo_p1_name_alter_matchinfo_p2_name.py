# Generated by Django 4.0.4 on 2022-04-17 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchdb_matches', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchinfo',
            name='p1_name',
            field=models.TextField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='matchinfo',
            name='p2_name',
            field=models.TextField(blank=True, default='', max_length=100),
        ),
    ]
