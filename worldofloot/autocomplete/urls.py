from django.conf.urls import patterns, url

urlpatterns = patterns('worldofloot.autocomplete.views',
    url(r'^(.*)$', 'complete', name='complete'),
)
