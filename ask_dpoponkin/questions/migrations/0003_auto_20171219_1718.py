# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-19 17:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20171218_2336'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='answer',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='question',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='liketoanswer',
            name='value',
            field=models.IntegerField(default=1, verbose_name='Value'),
        ),
        migrations.AddField(
            model_name='liketoquestion',
            name='value',
            field=models.IntegerField(default=1, verbose_name='Value'),
        ),
    ]
