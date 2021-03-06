# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _

from value.factors.models import Factor
from value.measures.models import MeasureValue
from value.deliverables.models import Deliverable, DecisionItemLookup
from value.deliverables.meetings.models import Meeting, MeetingItem, Scenario, Rationale, MeetingStakeholder
from value.deliverables.meetings.validators import validate_scenarios_selection


class AbstractMeetingForm(forms.ModelForm):
    deliverable = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Deliverable.objects.all(), required=True)
    name = forms.CharField(
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=255
    )
    started_at = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'class': 'form-control'}),
        label=_('Starting at'),
        input_formats=['%d/%m/%Y %H:%M', ]
    )
    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(attrs={'class': 'form-control expanding', 'rows': '1'}),
        max_length=2000,
        required=False
    )
    location = forms.CharField(
        label=_('Location'),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=50,
        required=False
    )


class NewMeetingForm(AbstractMeetingForm):
    default_evaluation = forms.ModelChoiceField(
        label=_('Default evaluation'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=MeasureValue.objects.none(),
        required=False
    )
    retrieve_evaluations = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label=_('Use decisions from past meetings')
    )

    class Meta:
        model = Meeting
        fields = ['deliverable', 'name', 'started_at', 'location', 'description', 'default_evaluation',
            'retrieve_evaluations', 'is_survey']

    def __init__(self, *args, **kwargs):
        super(NewMeetingForm, self).__init__(*args, **kwargs)
        self.fields['default_evaluation'].queryset = self.instance.deliverable.measure.measurevalue_set.all()


class MeetingForm(AbstractMeetingForm):
    class Meta:
        model = Meeting
        fields = ['deliverable', 'name', 'started_at', 'location', 'description', 'is_survey']


class MeetingStatusForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['status']


class MeetingItemFinalDecisionForm(forms.ModelForm):
    meeting_decision = forms.BooleanField(
        label=_('Meeting decision'),
        widget=forms.CheckboxInput(attrs={'class': 'final-decision'}),
        required=False
    )
    meeting_ranking = forms.FloatField(
        label=_('Meeting ranking'),
        widget=forms.TextInput(attrs={'class': 'form-control input-sm'}),
        required=False
    )

    class Meta:
        model = MeetingItem
        fields = ['meeting_decision', 'meeting_ranking']


class ScenarioForm(forms.ModelForm):
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    meeting_items = forms.ModelMultipleChoiceField(
        label=_('Meeting items'),
        widget=forms.CheckboxSelectMultiple(),
        queryset=None,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(ScenarioForm, self).__init__(*args, **kwargs)
        self.fields['meeting_items'].queryset = self.instance.meeting.meetingitem_set.all()

    class Meta:
        model = Scenario
        fields = ('name', 'meeting', 'meeting_items')


class FactorMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        if obj.group:
            return u'<strong>{0}</strong>: {1}'.format(escape(obj.group.name), escape(obj.name))
        return escape(obj.name)


class ScenarioBuilderForm(forms.Form):
    name = forms.CharField(label=_('Name'), max_length=255, required=True)
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    meeting_items_count = forms.ChoiceField(
        label=_('Number of decision items to compose the scenario'),
        required=True
    )
    factors = FactorMultipleModelChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        label=_('Related to'),
        queryset=Factor.objects.none(),
        required=True
    )
    criteria = forms.ModelChoiceField(label=_('Based on'), queryset=None, required=True, empty_label=None)

    def __init__(self, *args, **kwargs):
        super(ScenarioBuilderForm, self).__init__(*args, **kwargs)
        items_range = self.initial['meeting'].meetingitem_set.count()
        self.fields['meeting_items_count'].choices = [(choice, choice) for choice in range(1, items_range + 1)]
        self.fields['criteria'].queryset = self.initial['meeting'].measure.measurevalue_set.all()
        self.fields['factors'].queryset = self.initial['meeting'].factors.all()

    class Meta:
        fields = ('meeting', 'meeting_items_count', 'factors', 'criteria')


class CompareScenarioForm(forms.Form):
    meeting = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Meeting.objects.all(), required=True)
    scenarios = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        label=_('Select two scenarios to compare'),
        queryset=Scenario.objects.none(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(CompareScenarioForm, self).__init__(*args, **kwargs)
        self.fields['scenarios'].queryset = self.initial['meeting'].scenarios.all()
        self.fields['scenarios'].validators.append(validate_scenarios_selection)

    class Meta:
        fields = ('meeting', 'meeting_items')


class RationaleForm(forms.ModelForm):
    class Meta:
        model = Rationale
        fields = ['text', ]


class CompareStakeholdersOpinion(forms.Form):
    stakeholder_1 = forms.ModelChoiceField(queryset=User.objects.all())
    stakeholder_2 = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        fields = ('stakeholder_1', 'stakeholder_2', )


class DecisionAnalysisForm(forms.Form):
    value_factor_x = forms.ModelChoiceField(queryset=Factor.objects.none())
    value_factor_y = forms.ModelChoiceField(queryset=Factor.objects.none())
    size_z = forms.ModelChoiceField(
        queryset=DecisionItemLookup.objects.filter(column_type__in=(DecisionItemLookup.INTEGER,
                                                                    DecisionItemLookup.FLOAT))
    )
    scenario = forms.ModelChoiceField(queryset=Scenario.objects.none(), required=False)

    def __init__(self, meeting, *args, **kwargs):
        super(DecisionAnalysisForm, self).__init__(*args, **kwargs)
        self.fields['value_factor_x'].queryset = meeting.factors.all()
        self.fields['value_factor_y'].queryset = meeting.factors.all()
        self.fields['scenario'].queryset = meeting.scenarios.all()


class ScenarioFinalDecision(forms.Form):
    scenario = forms.ModelChoiceField(queryset=Scenario.objects.none(), required=False)

    def __init__(self, meeting, *args, **kwargs):
        super(ScenarioFinalDecision, self).__init__(*args, **kwargs)
        self.meeting = meeting
        self.fields['scenario'].queryset = meeting.scenarios.all()

    def set_final_decision(self):
        scenario = self.cleaned_data.get('scenario')
        self.meeting.meetingitem_set.update(meeting_decision=False)
        scenario.meeting_items.update(meeting_decision=True)


class AddStakeholdersForm(forms.Form):
    stakeholders = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        queryset=User.objects.none(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.meeting = kwargs.pop('meeting')
        super(AddStakeholdersForm, self).__init__(*args, **kwargs)
        self.fields['stakeholders'].queryset = User.objects \
            .exclude(id__in=self.meeting.meetingstakeholder_set.values('stakeholder__id'))

    @transaction.atomic
    def add_stakeholders(self):
        stakeholders = self.cleaned_data.get('stakeholders')
        for stakeholder in stakeholders:
            MeetingStakeholder.objects.get_or_create(stakeholder=stakeholder, meeting=self.meeting)
        self.meeting.calculate_progress()
        self.meeting.calculate_all_rankings()

    class Meta:
        fields = ('stakeholders',)
