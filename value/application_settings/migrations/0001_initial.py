# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSetting',
            fields=[
                ('name', models.CharField(max_length=255, serialize=False, primary_key=True, choices=[(b'EXCEL_SHEET_INDEX', b'Excel sheet index'), (b'EXCEL_ENTRY_ORIENTATION', b'Excel entry orientation'), (b'EXCEL_STARTING_ROW_COLUMN', b'Excel starting row/column'), (b'EXCEL_IMPORT_TEMPLATE', b'Excel import template'), (b'PLAIN_TEXT_SEPARATOR', b'Plain text separator'), (b'PLAIN_TEXT_STARTING_LINE', b'Plain text starting line'), (b'DECISION_ITEMS_DEFAULT_ORDERING', b'Decision items default ordering'), (b'DECISION_ITEMS_COLUMNS_DISPLAY', b'Decision items columns display')])),
                ('value', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'db_table': 'application_settings',
            },
        ),
    ]
