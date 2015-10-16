# coding: utf-8

from collections import OrderedDict

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from value.application_settings.models import ApplicationSetting
from value.factors.models import Factor
from value.measures.models import Measure


class Deliverable(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    stakeholders = models.ManyToManyField(User)
    measure = models.ForeignKey(Measure, related_name='deliverables')
    factors = models.ManyToManyField(Factor, related_name='deliverables')
    manager = models.ForeignKey(User, related_name='deliverable_manager_user')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='deliverable_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='deliverable_update_user')

    class Meta:
        db_table = 'deliverables'

    def __unicode__(self):
        return self.name

    def get_decision_items_fields(self):
        return DecisionItemLookup.get_visible_fields()

    def get_meetings_in_progress(self):
        return self.meeting_set.filter(status__in=['O', 'A'])

    def get_past_meetings(self):
        return self.meeting_set.filter(status='C')

    def get_stakeholders(self):
        stakeholders = self.stakeholders.all() | User.objects.filter(pk=self.manager.pk)
        return stakeholders


class DecisionItem(models.Model):
    deliverable = models.ForeignKey(Deliverable)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    column_1 = models.CharField(max_length=255, null=True, blank=True)
    column_2 = models.CharField(max_length=255, null=True, blank=True)
    column_3 = models.CharField(max_length=255, null=True, blank=True)
    column_4 = models.CharField(max_length=255, null=True, blank=True)
    column_5 = models.CharField(max_length=255, null=True, blank=True)
    column_6 = models.CharField(max_length=255, null=True, blank=True)
    column_7 = models.CharField(max_length=255, null=True, blank=True)
    column_8 = models.CharField(max_length=255, null=True, blank=True)
    column_9 = models.CharField(max_length=255, null=True, blank=True)
    column_10 = models.CharField(max_length=255, null=True, blank=True)
    column_11 = models.CharField(max_length=255, null=True, blank=True)
    column_12 = models.CharField(max_length=255, null=True, blank=True)
    column_13 = models.CharField(max_length=255, null=True, blank=True)
    column_14 = models.CharField(max_length=255, null=True, blank=True)
    column_15 = models.CharField(max_length=255, null=True, blank=True)
    column_16 = models.CharField(max_length=255, null=True, blank=True)
    column_17 = models.CharField(max_length=255, null=True, blank=True)
    column_18 = models.CharField(max_length=255, null=True, blank=True)
    column_19 = models.CharField(max_length=255, null=True, blank=True)
    column_20 = models.CharField(max_length=255, null=True, blank=True)
    column_21 = models.CharField(max_length=255, null=True, blank=True)
    column_22 = models.CharField(max_length=255, null=True, blank=True)
    column_23 = models.CharField(max_length=255, null=True, blank=True)
    column_24 = models.CharField(max_length=255, null=True, blank=True)
    column_25 = models.CharField(max_length=255, null=True, blank=True)
    column_26 = models.CharField(max_length=255, null=True, blank=True)
    column_27 = models.CharField(max_length=255, null=True, blank=True)
    column_28 = models.CharField(max_length=255, null=True, blank=True)
    column_29 = models.CharField(max_length=255, null=True, blank=True)
    column_30 = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'decision_items'

    def __unicode__(self):
        return self.name

    def has_attachments(self):
        return self.attachments.exists()


def attachment_file_upload_to(instance, filename):
    return u'deliverables/{0}/attachments/{1}'.format(instance.decision_item.deliverable.pk, filename)

class DecisionItemAttachment(models.Model):
    decision_item = models.ForeignKey(DecisionItem, related_name='attachments')
    attachment = models.FileField(upload_to=attachment_file_upload_to)
    
    class Meta:
        db_table = 'decision_items_attachments'

@receiver(post_delete, sender=DecisionItemAttachment)
def attachment_post_delete_handler(sender, **kwargs):
    attachment = kwargs['instance']
    storage, path = attachment.attachment.storage, attachment.attachment.path
    storage.delete(path)


class DecisionItemLookup(models.Model):
    STRING = 'S'
    FLOAT = 'F'
    INTEGER = 'I'
    DATE = 'D'
    DATE_TIME = 'T'
    COLUMN_TYPES = (
        (STRING, 'String'),
        (FLOAT, 'Float'),
        (INTEGER, 'Integer'),
        (DATE, 'Date'),
        (DATE_TIME, 'Date Time'),
        )

    column_name = models.CharField(max_length=255, primary_key=True)
    column_label = models.CharField(max_length=255, null=True, blank=True)
    column_type = models.CharField(max_length=1, choices=COLUMN_TYPES, default=STRING)
    column_display = models.BooleanField(default=True)

    class Meta:
        db_table = 'decision_items_lookup'

    def __unicode__(self):
        return self.column_name

    @staticmethod
    def get_base_fields():
        base_fields = {}
        base_fields['name'] = { 
                'label': 'Name', 
                'type': DecisionItemLookup.STRING, 
                'display': True }
        base_fields['description'] = { 
                'label': 'Description', 
                'type': DecisionItemLookup.STRING, 
                'display': True }
        return base_fields

    @staticmethod
    def get_custom_fields():
        fields = {}
        qs = DecisionItemLookup.objects.all()
        for result in qs:
            fields[result.column_name] = { 'label': result.column_label, 'type': result.column_type, 'display': result.column_display }
        return fields

    @staticmethod
    def get_all_fields():
        fields = dict(DecisionItemLookup.get_custom_fields().items() + DecisionItemLookup.get_base_fields().items())
        app_settings = ApplicationSetting.get()
        ordered_fields = OrderedDict()
        for key in app_settings[ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY]:
            if key in fields.keys():
                ordered_fields[key] = fields[key]
        for key in fields:
            if key not in ordered_fields.keys():
                ordered_fields[key] = fields[key]
        return ordered_fields

    @staticmethod
    def get_visible_fields():
        fields = dict(DecisionItemLookup.get_custom_fields().items() + DecisionItemLookup.get_base_fields().items())
        app_settings = ApplicationSetting.get()
        ordered_fields = OrderedDict()
        for key in app_settings[ApplicationSetting.DECISION_ITEMS_COLUMNS_DISPLAY]:
            if key in fields.keys():
                ordered_fields[key] = fields[key]
        return ordered_fields
