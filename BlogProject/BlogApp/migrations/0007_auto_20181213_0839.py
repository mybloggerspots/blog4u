# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-12-13 03:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('BlogApp', '0006_auto_20181206_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericStringTaggedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(db_index=True, max_length=50, verbose_name='Object id')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogapp_genericstringtaggeditem_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogapp_genericstringtaggeditem_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='BlogApp.GenericStringTaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
