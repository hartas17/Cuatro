# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-28 04:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190128_0432'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'managed': True},
        ),
        migrations.AlterModelTable(
            name='favorite',
            table='favorite',
        ),
        migrations.AlterModelTable(
            name='service',
            table='service',
        ),
    ]
