# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-30 12:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal', '0008_auto_20170618_2109'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPunchBlockType',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('long_name', models.CharField(db_index=True, max_length=50, verbose_name='название')),
                ('short_name', models.CharField(db_index=True, max_length=3, verbose_name='сокращение')),
                ('regexp', models.CharField(max_length=255, verbose_name='регулярное выражение')),
                ('is_station_group', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='группа станционного расположения')),
                ('number_group', models.PositiveSmallIntegerField(verbose_name='группа номера')),
                ('location_group', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='группа расположения')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical тип плинта',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='PunchBlockType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('long_name', models.CharField(max_length=50, unique=True, verbose_name='название')),
                ('short_name', models.CharField(max_length=3, unique=True, verbose_name='сокращение')),
                ('regexp', models.CharField(max_length=255, verbose_name='регулярное выражение')),
                ('is_station_group', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='группа станционного расположения')),
                ('number_group', models.PositiveSmallIntegerField(verbose_name='группа номера')),
                ('location_group', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='группа расположения')),
            ],
            options={
                'verbose_name_plural': 'типы плинтов',
                'verbose_name': 'тип плинта',
            },
        ),
    ]