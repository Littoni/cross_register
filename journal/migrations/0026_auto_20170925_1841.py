# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-25 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0025_auto_20170724_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crosspoint',
            name='child_class',
        ),
        migrations.RemoveField(
            model_name='historicalcrosspoint',
            name='child_class',
        ),
        migrations.RemoveField(
            model_name='historicalextensionbox',
            name='child_class',
        ),
        migrations.RemoveField(
            model_name='historicalpbxport',
            name='child_class',
        ),
        migrations.RemoveField(
            model_name='historicalphone',
            name='child_class',
        ),
        migrations.RemoveField(
            model_name='historicalpunchblock',
            name='child_class',
        ),
    ]