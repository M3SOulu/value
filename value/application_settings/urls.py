from django.conf.urls import patterns, include, url

urlpatterns = patterns('value.application_settings.views',
    url(r'^$', 'index', name='index'),
    url(r'^admins/$', 'admins', name='admins'),
    url(r'^items/$', 'items', name='items'),
    url(r'^items/save-ordering/$', 'save_ordering', name='save_ordering'),
    url(r'^items/save-import-templates/$', 'save_import_templates', name='save_import_templates'),
    url(r'^items/save-custom-fields/$', 'save_custom_fields', name='save_custom_fields'),
    url(r'^import/$', 'import_template', name='import'),
)
