# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 20:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0004_auto_20170517_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='selected_by',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
