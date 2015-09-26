# coding: utf-8

from django.db import models, transaction
from django.db.models import F, Count, Min, Sum
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed

from value.factors.models import Factor
from value.measures.models import Measure, MeasureValue
from value.deliverables.models import Deliverable, DecisionItem, Rationale
from value.deliverables.meetings.utils import format_percentage


class Meeting(models.Model):
    """
    Wraps all the information about a given meeting. The value-based decision-making process
    used in the tool occur per meeting. A meeting is associated with a deliverable, which
    can have many meeting. A meeting has a collection of stakeholders and a collection of
    decision items, defined by the classes MeetingItem and MeetingStakeholder.
    """
    ONGOING = u'O'
    CLOSED = u'C'
    STATUS = (
        (ONGOING, u'Ongoing'),
        (CLOSED, u'Closed'),
        )

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    deliverable = models.ForeignKey(Deliverable)
    status = models.CharField(max_length=1, choices=STATUS, default=ONGOING)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='meeting_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='meeting_update_user')    
    
    class Meta:
        ordering = ('-updated_at',)

    def __unicode__(self):
        return self.name

    def is_closed(self):
        return self.status == Meeting.CLOSED

    def get_status_label_html(self):
        if self.status == self.ONGOING:
            return u'<span class="label {0}"><span class="fa fa-refresh"></span> {1}</span>'.format("label-success", self.get_status_display().upper())
        elif self.status == self.CLOSED:
            return u'<span class="label {0}"><span class="fa fa-lock"></span> {1}</span>'.format("label-danger", self.get_status_display().upper())
        else:
            return u'<span class="label {0}">{1}</span>'.format("label-default", self.get_status_display().upper())

    def get_evaluations(self):
        return Evaluation.get_evaluations_by_meeting(self)

    def get_progress(self):
        """
        Returns the relative progress of a meeting, based on the count of the meeting's stakeholders,
        decision items and the deliverable's factors.
        The maximum number of possible evaluations is the product of multiplying 
        TotalEvaluations = MeetingStakeholders * MeetingItems * DeliverableFactors
        The total value is divided by the current number of evaluations, which can't be greater
        then TotalEvaluations.
        """
        stakeholders_count = self.meetingstakeholder_set.count()
        meeting_items_count = self.meetingitem_set.count()
        factors_count = Factor.list().count()

        max_evaluations = stakeholders_count * meeting_items_count * factors_count
        total_evaluations = self.get_evaluations().count()

        if max_evaluations != 0:
            percentage = round((total_evaluations / float(max_evaluations)) * 100.0, 2)
        else:
            percentage = 0.0

        return percentage

    def calculate_all_rankings(self):
        with transaction.atomic():
            for item in self.meetingitem_set.all():
                item.calculate_ranking()

    def get_stakeholder_groups(self):
        groups = Group.objects.all().order_by('name')
        grouped_stakeholders = { 'No group': [] }
        for group in groups:
            grouped_stakeholders[group.name] = []
        for meeting_stakeholder in self.meetingstakeholder_set.all().order_by('stakeholder__first_name'):
            groups = meeting_stakeholder.stakeholder.groups.all()
            if not groups.exists():
                grouped_stakeholders['No group'].append(meeting_stakeholder.stakeholder)
            else:
                for group in groups:
                    grouped_stakeholders[group.name].append(meeting_stakeholder.stakeholder)
        for name, stakeholders in grouped_stakeholders.items():
            if not any(stakeholders):
                del grouped_stakeholders[name]
        return grouped_stakeholders

    def get_ordered_meeting_items(self, order):
        """
        Order can represent regular meeting item fields and it's foreign keys.
        It's also possible to pass a MeasureValue id as parameter to order
        by the meeting item ranking.
        """
        meeting_items = self.meetingitem_set.all()
        can_order_in_db = order in ['decision_item__name', '-value_ranking']
        if can_order_in_db:
            meeting_items = meeting_items.order_by(order)
        else:
            ordered_by_ranking = Ranking.objects.filter(meeting_item__meeting=self, measure_value__id=order).order_by('-raw_votes')
            meeting_items = map(lambda item: item.meeting_item, ordered_by_ranking)
        return meeting_items


class MeetingItem(models.Model):
    meeting = models.ForeignKey(Meeting)
    decision_item = models.ForeignKey(DecisionItem)
    meeting_decision = models.BooleanField(default=False)
    rationales = models.ManyToManyField(Rationale)
    value_ranking = models.FloatField(default=0.0)
    meeting_ranking = models.FloatField(default=0.0)

    class Meta:
        ordering = ('decision_item__name',)

    def __unicode__(self):
        return '{0} ({1})'.format(self.decision_item.name, self.meeting.name)

    def get_value_ranking_display(self):
        return format_percentage(self.value_ranking)

    def value_ranking_as_html(self):
        formatted_ranking = self.get_value_ranking_display()
        if self.value_ranking < 0:
            return u'<strong class="text-danger">{0}</strong>'.format(formatted_ranking)
        elif self.value_ranking == 0:
            return u'<strong class="text-warning">{0}</strong>'.format(formatted_ranking)
        else:
            return u'<strong class="text-success">{0}</strong>'.format(formatted_ranking)

    def calculate_ranking(self):
        item_evaluations = Evaluation.get_evaluations_by_meeting(self.meeting) \
                .filter(meeting_item=self)

        measure = self.meeting.deliverable.measure
        stakeholders_count = self.meeting.meetingstakeholder_set.count()
        factors_count = Factor.list().count()
        max_evaluations = stakeholders_count * factors_count

        rankings = item_evaluations.values('measure_value__id').annotate(votes=Count('measure_value'))

        with transaction.atomic():

            for measure_value in measure.measurevalue_set.all():
                Ranking.objects.get_or_create(meeting_item=self, measure_value=measure_value)

            for ranking in rankings:
                votes = int(ranking['votes'])
                if max_evaluations != 0:
                    percentage = (votes / float(max_evaluations)) * 100.0
                else:
                    percentage = 0.0
                Ranking.objects.filter(meeting_item=self, measure_value__id=ranking['measure_value__id']).update(raw_votes=votes, percentage_votes=percentage)

            rankings = Ranking.objects.filter(meeting_item=self).order_by('measure_value__order')
            highest = rankings.first()
            lowest = rankings.last()
            self.value_ranking = highest.percentage_votes - lowest.percentage_votes
            self.save()


class Ranking(models.Model):
    """
    The ranking class is a convenience class, and also to reduce the detabase overhead.
    All the data stored by the Ranking class is calculated based on the Evaluation data.
    Saves for each MeetingItem, separeted by MeasureValue, the total number of votes and
    also the calculated percentage.
    """
    meeting_item = models.ForeignKey(MeetingItem)
    measure_value = models.ForeignKey(MeasureValue)
    raw_votes = models.IntegerField(default=0)
    percentage_votes = models.FloatField(default=0.0)

    class Meta:
        unique_together = (('meeting_item', 'measure_value',),)
        ordering = ('meeting_item__decision_item__description', 'measure_value__order')

    def __unicode__(self):
        return '{0} ({1}): {2}%'.format(self.meeting_item.decision_item.name, self.measure_value.description, self.percentage_votes)

    def get_percentage_votes_display(self):
        return round(self.percentage_votes, 2)


class MeetingStakeholder(models.Model):
    meeting = models.ForeignKey(Meeting)
    stakeholder = models.ForeignKey(User)
    meeting_input = models.FloatField(default=0.0)

    class Meta:
        ordering = ('stakeholder__first_name', 'stakeholder__last_name', 'stakeholder__username',)

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.stakeholder.username)


class Evaluation(models.Model):
    meeting = models.ForeignKey(Meeting)
    meeting_item = models.ForeignKey(MeetingItem)
    user = models.ForeignKey(User)
    factor = models.ForeignKey(Factor)
    measure = models.ForeignKey(Measure)
    measure_value = models.ForeignKey(MeasureValue, null=True, blank=True)
    evaluated_at = models.DateTimeField(null=True, blank=True)
    rationale = models.OneToOneField(Rationale, null=True)

    class Meta:
        unique_together = (('meeting', 'meeting_item', 'user', 'factor', 'measure'),)

    def __unicode__(self):
        return '{0} - {1}'.format(self.meeting.name, self.meeting_item.decision_item.name)

    @staticmethod
    def _list(meeting):
        qs = Evaluation.objects.filter(
            meeting=meeting, 
            factor__is_active=True, 
            measure__is_active=True).exclude(
            factor__measure=None).filter(
            factor__measure_id=F('measure_id'))
        return qs

    @staticmethod
    def get_evaluations_by_meeting(meeting):
        return Evaluation._list(meeting).exclude(measure_value=None)

    @staticmethod
    def get_user_evaluations_by_meeting(user, meeting):
        return Evaluation._list(meeting).filter(user=user)

class Scenario(models.Model):
    """
    The Scenario class is used to aggregate decision items to generate different 
    types of visualization inside the dashboard.
    """
    FACTORS = 'FACTORS'
    FACTORS_GROUPS = 'FACTORS_GROUPS'
    ACCEPTANCE = 'ACCEPTANCE'
    CATEGORIES = (
        (FACTORS, 'Factors Comparison'),
        (FACTORS_GROUPS, 'Factors Groups Comparison'),
        (ACCEPTANCE, 'Decision Items Acceptance'),
        )

    name = models.CharField(max_length=255)
    meeting = models.ForeignKey(Meeting, related_name='scenarios')
    category = models.CharField(max_length=14, choices=CATEGORIES, null=True, blank=True)
    meeting_items = models.ManyToManyField(MeetingItem)
    value_ranking = models.FloatField(default=0.0)

    class Meta:
        unique_together = (('name', 'meeting', 'category',),)

    def build(self, *args, **kwargs):
        limit = int(kwargs.get('meeting_items_count'))
        group = kwargs.get('factors_groups')
        measure_value = kwargs.get('criteria')

        evaluations = self.meeting.get_evaluations()
        scenario_items = evaluations.filter(measure_value=measure_value, factor__group=group) \
            .values_list('meeting_item', flat=True) \
            .annotate(count=Count('measure_value')) \
            .order_by('-count')[:limit]

        name = u'Scenario {0} {1} {2} Best Fit'.format(group.name, measure_value.description, measure_value.measure.name)
        with transaction.atomic():
            self.name = name
            self.save()
            self.meeting_items.add(*scenario_items)
        return self

    def get_value_ranking_display(self):
        return format_percentage(self.value_ranking)

def calculate_scenario_ranking(sender, **kwargs):
    action = kwargs.get('action')
    scenario = kwargs.get('instance')
    if action in ['post_add', 'post_remove']:
        meeting_items_count = scenario.meeting_items.count()
        result = scenario.meeting_items.aggregate(ranking=Sum('value_ranking'))
        meeting_items_ranking = result['ranking']
        if meeting_items_count > 0:
            scenario.value_ranking = meeting_items_ranking / float(meeting_items_count)
        else:
            scenario.value_ranking = 0.0
        scenario.save()

m2m_changed.connect(calculate_scenario_ranking, sender=Scenario.meeting_items.through)
