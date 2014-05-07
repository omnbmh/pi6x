# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template

from sdk import *

import urllib
#import urllib2
import json

# Create your views here.
ACCESS_TOKEN = "MTAwMDAxOTg0MTM5NTIxNTMwNzAwNw=="
def index(req):
    data = {}
    if 'event' in req.session:
        data = req.session['event']
    t = get_template('page/event_page/index.html')
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
    
def create(req):
    oauth = OAuth2Handler(auth_url = "")
    oauth.set_access_token(ACCESS_TOKEN)
    oauth.set_app_key_secret("123", "123", "123")
    oauth.set_openid("123")
    api = SosAPI(oauth)
    # local MTAwMDAxOTg0MTM5NTIxNTMwNzAwNw== 9841395215307007 outer  MTAwMDAxNjIxMTM4NTEyNjY1MTE3NQ== 6211385126651175
    create_json = api.get.call("event/create")(
        token=oauth.access_token,
        uid=9841395215307007,
        title = req.GET.get("title"),
        info = req.GET.get("info"),
        begin_at = req.GET.get("begin_at"),
        end_at = req.GET.get("end_at")
    )
    return HttpResponse(json.dumps(create_json), mimetype='text/json; charset=utf-8')
    
