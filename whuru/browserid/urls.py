from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^sign_in$', views.sign_in, name='whuru.browserid.sign_in'),
    url(r'^provision$', views.provision, name='whuru.browserid.provision'),
    url(r'^cert_key$', views.cert_key, name='whuru.browserid.cert_key'),
)
