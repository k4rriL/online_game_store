# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-19 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamedata', '0003_emailverificationtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='category',
            field=models.CharField(choices=[('SPO', 'Sports'), ('RAC', 'Racing'), ('RPG', 'RPG'), ('ACT', 'Action'), ('ADV', 'Adventure'), ('CAS', 'Casual'), ('STR', 'Strategy'), ('OTH', 'Other')], max_length=7),
        ),
    ]
