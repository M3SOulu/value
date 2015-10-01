# coding: utf-8

import json

from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction

from value.deliverables.models import Deliverable, DecisionItemLookup, DecisionItem
from value.deliverables.decorators import user_is_manager, user_is_stakeholder
from value.deliverables.meetings.models import Meeting, MeetingItem, MeetingStakeholder, Evaluation
from value.deliverables.meetings.forms import MeetingForm


@login_required
@user_is_stakeholder
def index(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    return render(request, 'deliverables/meetings.html', { 'deliverable': deliverable })

@login_required
@user_is_manager
def new(request, deliverable_id):
    deliverable = get_object_or_404(Deliverable, pk=deliverable_id)
    decision_items_fields = DecisionItemLookup.get_visible_fields()
    decision_items = deliverable.decisionitem_set.all()
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        stakeholder_ids = request.POST.getlist('stakeholders')
        selected_stakeholders = User.objects.filter(id__in=stakeholder_ids)
        meeting_stakeholders = User.objects.filter(Q(id__in=selected_stakeholders) | Q(id__in=deliverable.stakeholders.all())).filter(is_active=True).distinct()

        decision_item_ids = request.POST.getlist('decision_item')
        selected_decision_items = deliverable.decisionitem_set.filter(id__in=decision_item_ids)

        if form.is_valid() and selected_stakeholders.exists() and selected_decision_items.exists():
            form.instance.deliverable = deliverable
            form.instance.created_by = request.user
            meeting = form.save()

            for stakeholder in selected_stakeholders:
                meeting_stakeholder = MeetingStakeholder()
                meeting_stakeholder.meeting = meeting
                meeting_stakeholder.stakeholder = stakeholder
                meeting_stakeholder.save()

            for decision_item in selected_decision_items:
                meeting_item = MeetingItem()
                meeting_item.meeting = meeting
                meeting_item.decision_item = decision_item
                meeting_item.save()

            deliverable.save()
            messages.success(request, u'The meeting {0} was created successfully.'.format(meeting.name))
            return redirect(reverse('deliverables:meetings:meeting', args=(deliverable.pk, meeting.pk,)))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeetingForm()
        meeting_stakeholders = deliverable.stakeholders.filter(is_active=True).order_by('first_name', 'last_name', 'username')
        selected_stakeholders = meeting_stakeholders
        selected_decision_items = decision_items
    available_stakeholders = User.objects \
            .exclude(id__in=deliverable.stakeholders.all()) \
            .exclude(id__in=selected_stakeholders) \
            .filter(is_active=True) \
            .order_by('first_name', 'last_name', 'username')
    return render(request, 'meetings/new.html', { 
        'deliverable': deliverable,
        'decision_items_fields': decision_items_fields,
        'decision_items': decision_items,
        'selected_decision_items': selected_decision_items,
        'form': form,
        'meeting_stakeholders': meeting_stakeholders,
        'available_stakeholders': available_stakeholders,
        'selected_stakeholders': selected_stakeholders
        })

@login_required
def meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if meeting.is_closed():
        return redirect(reverse('deliverables:meetings:final_decision', args=(deliverable_id, meeting_id)))
    else:
        return redirect(reverse('deliverables:meetings:evaluate', args=(deliverable_id, meeting_id)))

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def close_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.status = Meeting.CLOSED
    meeting.save()
    meeting.deliverable.save()
    messages.success(request, u'The meeting {0} was closed successfully.'.format(meeting.name))
    return redirect(reverse('deliverables:meetings:meeting', args=(meeting.deliverable.pk, meeting.pk)))

@login_required
@user_passes_test(lambda user: user.is_superuser)
@require_POST
def open_meeting(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    meeting.status = Meeting.ONGOING
    meeting.save()
    meeting.deliverable.save()
    messages.success(request, u'The meeting {0} was opened successfully.'.format(meeting.name))
    return redirect(reverse('deliverables:meetings:meeting', args=(meeting.deliverable.pk, meeting.pk)))

@login_required
@require_POST
def remove_stakeholder(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_id = request.POST.get('stakeholder')
    user = User.objects.get(pk=stakeholder_id)
    if user != request.user:
        meeting_stakeholder = MeetingStakeholder.objects.get(stakeholder=user, meeting=meeting)
        meeting_stakeholder.delete()
        Evaluation.get_user_evaluations_by_meeting(user, meeting).delete()
        meeting.calculate_all_rankings()
        messages.success(request, u'{0} was successfully removed from the meeting!'.format(user.profile.get_display_name()))
    else:
        messages.warning(request, 'You cannot remove yourself from the meeting.')
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def add_stakeholders(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    stakeholder_ids = request.POST.getlist('stakeholders')
    if any(stakeholder_ids):
        for stakeholder_id in stakeholder_ids:
            user = User.objects.get(pk=stakeholder_id)
            meeting_stakeholder = MeetingStakeholder(stakeholder=user, meeting=meeting)
            meeting_stakeholder.save()
        meeting.calculate_all_rankings()
        messages.success(request, u'Stakeholders sucessfully added to the meeting!')
    else:
        messages.warning(request, u'Select at least one stakeholder to add.')
    return redirect(reverse('deliverables:meetings:stakeholders', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def remove_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    meeting_items_ids = request.POST.getlist('meeting_items')
    if any(meeting_items_ids):
        meeting.meetingitem_set.filter(id__in=meeting_items_ids).delete()
        meeting.calculate_all_rankings()
        messages.success(request, u'Decision items sucessfully removed from the meeting!')
    else:
        messages.warning(request, u'Select at least one decision item to remove.')
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))

@login_required
@require_POST
@transaction.atomic
def add_decision_items(request, deliverable_id, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_ids = request.POST.getlist('decision_items')
    if any(decision_items_ids):
        for decision_item_id in decision_items_ids:
            decision_item = DecisionItem.objects.get(pk=decision_item_id)
            meeting_item = MeetingItem(meeting=meeting, decision_item=decision_item)
            meeting_item.save()
        meeting.calculate_all_rankings()
        messages.success(request, u'Decision items sucessfully added to the meeting!')
    else:
        messages.warning(request, u'Select at least one decision item to add.')
    return redirect(reverse('deliverables:meetings:decision_items', args=(deliverable_id, meeting_id)))

@login_required
def settings(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            meeting.deliverable.save()
            messages.success(request, u'The meeting details was saved successfully!')
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'meetings/settings/details.html', {
            'meeting': meeting,
            'form': form
            })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def decision_items(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    decision_items_in_use = meeting.meetingitem_set.values('decision_item__id')
    available_decision_items = meeting.deliverable.decisionitem_set.exclude(id__in=decision_items_in_use)
    return render(request, 'meetings/settings/items.html', { 
            'meeting': meeting, 
            'available_decision_items': available_decision_items
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def stakeholders(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    stakeholders = [meeting_stakeholder.stakeholder for meeting_stakeholder in meeting.meetingstakeholder_set.select_related('stakeholder')]
    available_stakeholders = User.objects \
            .exclude(id__in=meeting.meetingstakeholder_set.values('stakeholder__id')) \
            .filter(is_active=True) \
            .order_by('first_name', 'last_name', 'username')
    return render(request, 'meetings/settings/stakeholders.html', { 
            'meeting': meeting,
            'stakeholders': stakeholders,
            'available_stakeholders': available_stakeholders,
        })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, deliverable_id, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id, deliverable__id=deliverable_id)
    if request.method == 'POST':
        meeting.delete()
        messages.success(request, u'The meeeting {0} was completly deleted successfully.'.format(meeting.name))
        return redirect(reverse('deliverables:deliverable', args=(meeting.deliverable.pk,)))
    else:
        return render(request, 'meetings/settings/delete.html', { 'meeting': meeting })