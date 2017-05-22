# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 15:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aparcamientos', '0013_aparcamiento_numero_comentarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='estilo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
