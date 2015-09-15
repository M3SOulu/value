# coding: utf-8

from django import forms

from value.factors.models import Factor, Group
from value.measures.models import Measure


class BaseFactorForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'expanding', 'rows': '3'}), max_length=2000, required=False)
    measure = forms.ModelChoiceField(widget=forms.Select(attrs={'style': 'width: 50%'}), queryset=Measure.objects.filter(is_active=True), empty_label='Select...', required=False)
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'style': 'width: 50%'}), queryset=Group.objects.all(), empty_label='Select...', required=False)
    
    class Meta:
        model = Factor
        fields = ('name', 'description', 'measure', 'group')

class CreateFactorForm(BaseFactorForm):
    pass

class ChangeFactorForm(BaseFactorForm):
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(), 
        label='Active',
        help_text='Unselect this instead of deleting factors.',
        required=False)

    class Meta:
        model = Factor
        fields = ('name', 'description', 'measure', 'group', 'is_active')

class GroupForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}), max_length=255)

    class Meta:
        model = Group
        fields = ['name',]
