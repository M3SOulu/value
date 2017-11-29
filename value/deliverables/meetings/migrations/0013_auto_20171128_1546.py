# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-11-28 15:46
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_meeting_meeting_decision_rationale'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='is_survey',
            field=models.BooleanField(default=False, verbose_name='accept external input?'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='survey_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]