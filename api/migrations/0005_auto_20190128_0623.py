# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-28 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190128_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=255),
        ),
    ]
