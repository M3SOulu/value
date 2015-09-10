# coding: utf-8

from django.conf.urls import patterns, include, url


urlpatterns = patterns('value.users.groups.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(\d+)/$', 'edit', name='edit'),
    url(r'^(\d+)/delete/$', 'delete', name='delete'),
)