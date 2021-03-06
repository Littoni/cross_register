# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-14 10:27
from __future__ import unicode_literals

from django.db import migrations


def get_parent(crosspoint, apps):
    from django.db import connection

    PBXPort = apps.get_model('journal', 'PBXPort')

    src = None

    with connection.cursor() as cursor:
        sql = '''
            WITH RECURSIVE
            Rec (id, source_id, location_id)
            AS (
                  SELECT *, id AS main_id
                    FROM journal_crosspoint
                   WHERE source_id IS NULL
                UNION ALL
                  SELECT cp.*, r.main_id AS main_id
                    FROM Rec r
                    JOIN journal_crosspoint cp ON (r.id = cp.source_id)
            )
            SELECT main_id
              FROM Rec
             WHERE id = {}
        '''

        cursor.execute(sql.format(crosspoint.pk))

        row = cursor.fetchone()
        try:
            src = PBXPort.objects.get(pk=row[0])
        except:
            pass

    return src


def populate_locations_main_source(apps, schema_editor):
    CrossPoint = apps.get_model('journal', 'CrossPoint')
    PBXPort = apps.get_model('journal', 'PBXPort')

    for cp in CrossPoint.objects.filter(source__isnull=False):
        cp.main_source = get_parent(cp, apps)
        cp.save()

    for pbxport in PBXPort.objects.filter(subscriber_number__isnull=False):
        pbxport.main_source = pbxport
        pbxport.save()


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0016_auto_20170714_1327'),
    ]

    operations = [
        migrations.RunPython(
            populate_locations_main_source,
            reverse_code=lambda *args: None,
        ),
    ]
