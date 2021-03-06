# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-10 08:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0009_auto_20170709_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpbx',
            name='description',
            field=models.CharField(blank=True, max_length=30, verbose_name='примечание'),
        ),
        migrations.AddField(
            model_name='historicalpbx',
            name='location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='journal.Location'),
        ),
        migrations.AddField(
            model_name='pbx',
            name='description',
            field=models.CharField(blank=True, max_length=30, verbose_name='примечание'),
        ),
        migrations.AddField(
            model_name='pbx',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='journal.Location', verbose_name='расположение'),
        ),
    ]
