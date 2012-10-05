from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^login.json$', views.login_json, name='whuru.profiles.login_json'),
)
