# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0015_aparcamiento_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='aparcamiento',
            name='numero',
            field=models.IntegerField(null=True),
        ),
    ]
