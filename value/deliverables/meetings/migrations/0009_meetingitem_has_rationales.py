# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_meeting_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingitem',
            name='has_rationales',
            field=models.BooleanField(default=False),
        ),
    ]
