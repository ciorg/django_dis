# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-21 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_project_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='priority',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='priority',
            field=models.IntegerField(),
        ),
    ]
