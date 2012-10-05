import logging
import os.path

import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from funfactory.urlresolvers import get_url_prefix, set_url_prefix, reverse, Prefixer

from session_csrf import anonymous_csrf
import whuru.settings
from django.conf import settings


def well_known_browserid(request):
    # HACK: The following code is terrible. But, I really wanted some
    # locale-free URLs, in order to force a locale redirect later.
    op = get_url_prefix()
    np = Prefixer(request)
    np.locale = 'XXX'
    set_url_prefix(np)
    authentication_url=reverse('whuru.browserid.sign_in').replace('/XXX','')
    provisioning_url=reverse('whuru.browserid.provision').replace('/XXX','')
    set_url_prefix(op)

    settings_root = os.path.dirname(whuru.settings.__file__)
    public_key_fn = os.path.join(settings_root, 'key.publickey')
    public_key = open(public_key_fn, 'rb').read()

    resp = render(request, 'browserid/well-known-browserid.json', dict(
        public_key=public_key,
        authentication_url=authentication_url,
        provisioning_url=provisioning_url,
    ))
    resp['Content-Type'] = 'application/json'
    return resp

def sign_in(request):
    email = request.REQUEST.get('email', False)

    resp = render(request, 'browserid/sign_in.html', dict(
        email = email
    ))
    resp['x-frame-options'] = 'ALLOW'
    return resp

def provision(request):
    data = {}
    if request.user.is_authenticated():
        username = request.user.username
        data['expected_id'] = settings.PERSONA_ID_TMPL % username
    resp = render(request, 'browserid/provision.html', data)
    resp['x-frame-options'] = 'ALLOW'
    return resp

@csrf_exempt
def cert_key(request):
    """Proxy key certification to a browserid-certifier service instance, until
    or unless I figure out how to do this entirely in Python."""
    resp = HttpResponse()
    resp['Content-Type'] = 'application/json; charset=utf-8'
    if not request.user.is_authenticated():
        resp.write(simplejson.dumps({
            "success": False,
            "reason": "UNAUTHENTICATED"
        }))
    else:
        try:
            username = request.user.username or 'lmorchard'
            data = simplejson.loads(request.body)
            to_cert = simplejson.dumps({
                # grumble,grumble...
                "pubkey": simplejson.dumps(data['pubkey']),
                "duration": data['duration'],
                "email": settings.PERSONA_ID_TMPL % username
            })
            cert_resp = requests.post(
                settings.PERSONA_CERTIFIER_URL,
                data=to_cert,
                headers={'Content-Type':'application/json; charset=utf-8'}
            )
            resp.write(cert_resp.text)
        except Exception, e:
            resp.write(simplejson.dumps({
                "success": False,
                "reason": "UNEXPECTED"
            }))
    return resp
