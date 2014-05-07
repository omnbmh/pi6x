from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template

import urllib
import json

# Create your views here.

def index(req):
    data = {}
    if 'event54' in req.session:
        data = req.session['event54']
    t = get_template('event54.html')
    c = template.Context(data)
    return HttpResponse(t.render(c))
    
def authorize(req):
    uid = req.GET.get('uid')
    postDict = {
        'app_key':100002,
        'app_secret':'ef1302e559c65f91864ada2ff1fe6b27',
        'uid':uid
    }
    postData = urllib.urlencode(postDict);
    request = urllib2.Request('http://192.168.8.3:8080/sos-api/oauth2/access_token',postData)
    request.add_header('Content-Type', "application/x-www-form-urlencoded")
    s = urllib2.urlopen(request).read()
    j = json.loads(s)
    # print j['result']
    # wirite session
    req.session['event54'] = j['result']
    return HttpResponseRedirect('./')
