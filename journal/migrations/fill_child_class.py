# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 15:38
from __future__ import unicode_literals

from django.db import migrations, models


def fill_child_classes(apps, schema_editor):
    CrossPoint = apps.get_model('journal', 'CrossPoint')

    for cp in CrossPoint.objects.all():
        result = None

        for cp_subclass in CrossPoint.__subclasses__():
            try:
                cp_subclass.objects.get(crosspoint_ptr=cp.pk)
                result = cp_subclass
            except models.ObjectDoesNotExist as e:
                pass

        cp.child_class = result.__name__
        cp.save_without_historical_record()


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0014_auto_20170622_1652'),
    ]

    operations = [
        migrations.RunPython(fill_child_classes)
    ]