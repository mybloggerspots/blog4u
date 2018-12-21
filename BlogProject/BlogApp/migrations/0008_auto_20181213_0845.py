# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-12-13 03:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('BlogApp', '0007_auto_20181213_0839'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='genericstringtaggeditem',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='genericstringtaggeditem',
            name='tag',
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='BlogApp.TaggedPost', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.DeleteModel(
            name='GenericStringTaggedItem',
        ),
        migrations.AddField(
            model_name='taggedpost',
            name='content_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.Post'),
        ),
        migrations.AddField(
            model_name='taggedpost',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogapp_taggedpost_items', to='taggit.Tag'),
        ),
    ]