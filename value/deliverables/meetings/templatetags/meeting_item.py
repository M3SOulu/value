# coding: utf-8

from django import template
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from value.deliverables.meetings.models import MeetingItem
from value.deliverables.meetings.utils import format_percentage

register = template.Library()


@register.filter('meeting_item')
def meeting_item(meeting_item_id):
    try:
        item = MeetingItem.objects.get(pk=meeting_item_id)
        return item
    except MeetingItem.DoesNotExist:
        return None


@register.simple_tag
def display_evaluation_summary(instance):
    html = u'''<div class="progress help-cursor"
                    style="margin-bottom: 0"
                    data-toggle="tooltip"
                    data-container="body"
                    data-placement="top"
                    title="{0}">'''.format(
        _('Decision&nbsp;Item&nbsp;Evaluation&nbsp;Summary')
    )

    evaluation_summary = instance.evaluation_summary.all().select_related('measure_value')
    for ranking in evaluation_summary:
        progress_bar = u'''<div class="progress-bar" style="width: {0}%; background-color: {1};">
          <span class="measure-percent" data-measure-id="{2}" data-percentage="{0}">{3}</span>%
        </div>'''.format(ranking.percentage_votes,
                         ranking.measure_value.color,
                         ranking.measure_value.pk,
                         ranking.get_percentage_votes_display())
        html += progress_bar

    html += u'</div>'
    return mark_safe(html)


@register.simple_tag
def display_ranking_label(ranking):
    label = 'label-success'
    if ranking < 0:
        label = 'label-danger'
    elif ranking == 0:
        label = 'label-warning'
    html = u'''<span class="label {0} pull-right help-cursor"
                     data-toggle="tooltip"
                     data-container="body"
                     data-placement="top"
                     style="margin-right: 10px; margin-top: 2px;"
                     title="{1}">{2}</span>'''.format(
        label,
        _('Value Ranking'),
        format_percentage(ranking)
    )
    return mark_safe(html)


@register.simple_tag
def display_info_button(decision_item):
    remote = reverse(
        'deliverables:details_decision_item',
        args=(decision_item.deliverable.pk, decision_item.pk)
    )
    html = u'''
        <span data-toggle="tooltip"
              title="{0}"
              data-container="body" style="margin-left: 5px;">
          <a href="javascript:void(0);"
             class="btn-details js-decision-item-details"
             data-toggle="modal"
             data-target="#modal-decision-item-details"
             data-remote-url="{1}">
            <span class="glyphicon glyphicon-info-sign"></span>
          </a>
    </span>'''.format(_('Click to view details'), remote)
    return mark_safe(html)


@register.simple_tag
def display_rationales_button(meeting_item):
    remote = reverse(
        'deliverables:meetings:meeting_item_rationale',
        args=(meeting_item.decision_item.deliverable.pk, meeting_item.meeting.pk, meeting_item.pk)
    )
    color = '#333333'
    if meeting_item.has_rationales:
        color = '#337ab7'

    html = u'''
        <span data-toggle="tooltip"
              title="{0}"
              data-container="body" style="margin-left: 5px;">
          <a href="javascript:void(0);"
             class="btn-details js-meeting-item-rationale"
             data-toggle="modal"
             data-target="#modal-rationale"
             data-remote-url="{1}"
             style="color: {2}!important;">
            <span class="fa fa-comments"></span>
          </a>
    </span>'''.format(_('Click to view comments'), remote, color)
    return mark_safe(html)
