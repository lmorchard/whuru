import logging
import os.path

import requests

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from session_csrf import anonymous_csrf
from django.conf import settings


@require_POST
@csrf_exempt
def login_json(request):
    resp = HttpResponse()
    resp['Content-Type'] = 'application/json; charset=utf-8'
    try:
        data = simplejson.loads(request.body)
        user = authenticate(username=data['username'],
                            password=data['password'])
        if user:
            login(request, user)
            out = { "success": True, "username": user.username }
        else:
            out = { "success": False, "reason": "AUTH_FAILED" }
    except Exception, e:
        out = { "success": False, "reason": "UNEXPECTED %s" % e }
    resp.write(simplejson.dumps(out))
    return resp
