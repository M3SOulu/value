from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'value.core.views.home', name='home'),
    url(r'^signin/$', 'django.contrib.auth.views.login', { 'template_name' : 'core/signin.html' }, name='signin'),
    url(r'^signout/$', 'django.contrib.auth.views.logout', { 'next_page' : '/' }, name='signout'),
    url(r'^account/$', 'value.users.views.account', name='account'),
    url(r'^account/password/$', 'value.users.views.change_password', name='change_password'),
    url(r'^factors/', include('value.factors.urls', namespace='factors')),
    url(r'^measures/', include('value.measures.urls', namespace='measures')),
    url(r'^users/', include('value.users.urls', namespace='users')),
    url(r'^help/', include('value.help.urls', namespace='help')),
    url(r'^deliverable/', include('value.workspace.urls', namespace='workspace')),
    url(r'^avatar/', include('value.djavatar.urls')),
)
