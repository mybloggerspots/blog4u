# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-12-05 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0005_auto_20181206_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('politics', 'Politics'), ('business', 'Business'), ('sports', 'Sports'), ('films', 'Films'), ('technology', 'Technology')], default=None, max_length=20),
        ),
    ]
