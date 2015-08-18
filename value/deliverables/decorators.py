from functools import wraps

from django.core.urlresolvers import reverse as r
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

from value.deliverables.models import Deliverable
from value.deliverables.meetings.models import Meeting

def permission_denied(request):
    if request.is_ajax():
        return HttpResponseForbidden()
    else:
        return redirect(r('signin'))

def user_is_manager(function):

    def wrap(request, *args, **kwargs):
        try:
            deliverable = Deliverable.objects.get(pk=kwargs['deliverable_id'])
            if deliverable.manager == request.user:
                return function(request, *args, **kwargs)
            else:
                return permission_denied(request)
        except Deliverable.DoesNotExist:
            return permission_denied(request)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap