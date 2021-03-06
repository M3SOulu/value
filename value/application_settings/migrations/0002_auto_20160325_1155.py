# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationsetting',
            name='name',
            field=models.CharField(choices=[(b'EXCEL_SHEET_INDEX', 'Excel sheet index'), (b'EXCEL_ENTRY_ORIENTATION', 'Excel entry orientation'), (b'EXCEL_STARTING_ROW_COLUMN', 'Excel starting row/column'), (b'EXCEL_IMPORT_TEMPLATE', 'Excel import template'), (b'PLAIN_TEXT_SEPARATOR', 'Plain text separator'), (b'PLAIN_TEXT_STARTING_LINE', 'Plain text starting line'), (b'DECISION_ITEMS_DEFAULT_ORDERING', 'Decision items default ordering'), (b'DECISION_ITEMS_COLUMNS_DISPLAY', 'Decision items columns display')], max_length=255, primary_key=True, serialize=False, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='applicationsetting',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='value'),
        ),
    ]
