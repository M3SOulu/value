# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 14:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20160321_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='factor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='factors.Factor'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='measure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='measures.Measure'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='measure_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='measures.MeasureValue'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meetings.Meeting'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='meeting_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meetings.MeetingItem'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='rationale',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='meetings.Rationale'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meetings_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='deliverable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='deliverables.Deliverable'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='measure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='meetings', to='measures.Measure'),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='meetings_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='meetingitem',
            name='decision_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='deliverables.DecisionItem'),
        ),
        migrations.AlterField(
            model_name='meetingitem',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meetings.Meeting'),
        ),
        migrations.AlterField(
            model_name='meetingstakeholder',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meetings.Meeting'),
        ),
        migrations.AlterField(
            model_name='meetingstakeholder',
            name='stakeholder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='measure_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='measures.MeasureValue'),
        ),
        migrations.AlterField(
            model_name='ranking',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='meetings.Meeting'),
        ),
        migrations.AlterField(
            model_name='rationale',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rationales_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rationale',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rationales_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='scenarios', to='meetings.Meeting'),
        ),
    ]
