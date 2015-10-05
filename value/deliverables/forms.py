# coding: utf-8

from django import forms
from django.contrib.auth.models import User

from value.factors.models import Factor
from value.measures.models import Measure
from value.deliverables.models import Deliverable, Rationale


class StakeholderPanelGroupMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = obj.profile.get_display_name()
        if obj.groups.exists():
            groups = ''
            for group in obj.groups.all():
                groups += u'{0}, '.format(group.name)
            groups = groups[:-2]
            name = u'{0} <small class="text-muted">({1})</small>'.format(name, groups)
        return name

class FactorModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        name = obj.name
        if obj.group:
            name = u'{0} <small class="text-muted">({1})</small>'.format(obj.name, obj.group.name)
        if not obj.is_active:
            name = u'<span class="text-danger">{0} <small><strong>inactive</strong></small></span>'.format(name)
        return name


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DeliverableForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)
    stakeholders = StakeholderPanelGroupMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username'), 
        required=False
        )
    factors = FactorModelMultipleChoiceField(
        label='Select value factors to be used within the decision-making meetings',
        widget=forms.CheckboxSelectMultiple(), 
        queryset=Factor.objects.filter(is_active=True), 
        required=True
        )
    measure = forms.ModelChoiceField(label='Select the measure to be used within the decision-making meetings', 
        queryset=Measure.objects.filter(is_active=True),
        required=True,
        empty_label=None)

    class Meta:
        model = Deliverable
        fields = ['name', 'description', 'stakeholders', 'factors', 'measure']


class DeliverableBasicDataForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control expanding', 'rows': '1'}), max_length=2000, required=False)

    class Meta:
        model = Deliverable
        fields = ['name', 'description',]

        
class RationaleForm(forms.ModelForm):
    class Meta:
        model = Rationale
        fields = ['text',]


class DeliverableFactorsForm(forms.ModelForm):
    factors = FactorModelMultipleChoiceField(
        label='Select value factors to be used within the decision-making meetings',
        widget=forms.CheckboxSelectMultiple(), 
        queryset=Factor.objects.all(), 
        required=True
        )

    class Meta:
        model = Deliverable
        fields = ['factors',]


class DeliverableMeasureForm(forms.ModelForm):
    measure = forms.ModelChoiceField(label='Select the measure to be used within the decision-making meetings', 
        queryset=Measure.objects.all(),
        required=True,
        empty_label=None)
    class Meta:
        model = Deliverable
        fields = ['measure',]
