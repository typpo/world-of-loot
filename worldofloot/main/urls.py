from django.conf.urls import patterns, url

urlpatterns = patterns('worldofloot.main.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/(.*)', 'index', name='index'),
    url(r'^info/(.*)', 'get_item_info', name='get_item_info'),
)
