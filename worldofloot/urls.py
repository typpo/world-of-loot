from django.conf.urls.defaults import *
from django.views.static import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('worldofloot.main.urls')),
    (r'^autocomplete/', include('worldofloot.autocomplete.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    #(r'^admin/', include('django.contrib.admin.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
    #(r'^accounts/', include('registration.urls')),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT}),
)
