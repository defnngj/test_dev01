# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-12 18:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0009_golbalvaluesmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcasemodel',
            name='valuePicker',
            field=models.TextField(default=''),
        ),
    ]
