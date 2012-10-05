from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from funfactory.monkeypatches import patch
patch()

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template',
       {'template': 'index.html'}),

    (r'^.well-known/browserid$', 'whuru.browserid.views.well_known_browserid'),
    (r'^', include('wellknown.urls')),
    (r'^webfinger/', include('webfinger.urls')),
    (r'^browserid/', include('whuru.browserid.urls')),
    (r'^profiles/', include('whuru.profiles.urls')),
    (r'^profiles/', include('registration.backends.default.urls')),
    
    # Generate a robots.txt
    (r'^robots\.txt$', 
        lambda r: HttpResponse(
            "User-agent: *\n%s: /" % 'Allow' if settings.ENGAGE_ROBOTS else 'Disallow' ,
            mimetype="text/plain"
        )
    ),

    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
