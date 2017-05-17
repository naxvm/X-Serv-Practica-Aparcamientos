# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aparcamientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aparcamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('hora', models.DateTimeField()),
                ('aparcamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aparcamientos.Aparcamiento')),
            ],
        ),
    ]