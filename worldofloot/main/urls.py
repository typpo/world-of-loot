from django.conf.urls import patterns, url

urlpatterns = patterns('worldofloot.main.views',
    url(r'^$', 'index', name='index'),
)
