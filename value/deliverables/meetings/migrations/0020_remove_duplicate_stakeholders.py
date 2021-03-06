# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-02-11 11:51
from __future__ import unicode_literals

from django.db import migrations, transaction


@transaction.atomic
def remove_duplicates(apps, schema_editor):
    Meeting = apps.get_model('meetings', 'Meeting')
    MeetingStakeholder = apps.get_model('meetings', 'MeetingStakeholder')

    for meeting in Meeting.objects.all():
        queryset = meeting.meetingstakeholder_set.values_list('stakeholder_id', flat=True)
        count = queryset.count()
        distinct_count = queryset.distinct().count()
        if count != distinct_count:
            deliverable_stakeholders = list(meeting.deliverable.stakeholders.values_list('id', flat=True))
            meeting_stakeholders = list(queryset.distinct())
            meeting.meetingstakeholder_set.all().delete()
            for user_id in meeting_stakeholders:
                meeting_stakeholder = MeetingStakeholder.objects.create(
                    meeting=meeting,
                    stakeholder_id=user_id,
                    is_external=(user_id not in deliverable_stakeholders)
                )

                evaluations_count = meeting.evaluation_set \
                    .filter(user_id=user_id, factor__in=meeting.factors.all(), measure=meeting.measure) \
                    .exclude(measure_value=None) \
                    .count()

                factors_count = meeting.factors.count()
                meeting_items_count = meeting.meetingitem_set.count()
                max_input = factors_count * meeting_items_count

                percentage = 0.0
                if max_input != 0:
                    percentage = (evaluations_count / float(max_input)) * 100.0
                    percentage = round(percentage, 2)

                meeting_stakeholder.meeting_input = percentage
                meeting_stakeholder.save()


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0019_auto_20181120_0838'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates),
    ]
