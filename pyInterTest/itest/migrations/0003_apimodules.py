# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itest', '0002_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiModules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itest.Project')),
            ],
        ),
    ]
