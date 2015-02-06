# encoding='utf-8'

import time
import json

from django import template
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template.loader import get_template

#from tweibo import *

__author__ = 'Chen Dezhi (c8d8z8@gmail.com)'
__version__ = '1.0'

# weibo app config
APP_KEY = '100628862'
APP_SECRET = '021e18ea097817f15a819a45c0e5c592'

REDIRECT_URL = 'http://127.0.0.1:8888/api/auth/callback'
#REDIRECT_URL = 'http://192.168.8.102:8888/api/auth/callback'
#REDIRECT_URL = 'http://gae-django-py-weibo.appspot.com/api/auth/callback'
#REDIRECT_URL = 'http://qqvs360.duapp.com/api/auth/callback'

'''
授权后设置授权信息
ACCESS_TOKEN = "c3337750b56e1ee3d35e669ebdea0eef"
OPENID = "99A960D0C781A65640DD2A1BE48CCD6A"
'''
ACCESS_TOKEN = "c3337750b56e1ee3d35e669ebdea0eef"
OPENID = "99A960D0C781A65640DD2A1BE48CCD6A"

# 返回text是unicode，设置默认编码为utf8
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

def auth_login(req):
    oauth2 = OAuth2Handler()
    oauth2.set_app_key_secret(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
    return HttpResponseRedirect(oauth2.get_authorize_url())
    
def auth_callback(req):
    code = req.GET.get('code')
    openkey = req.GET.get('openkey')
    
    oauth2 = OAuth2Handler()
    oauth2.set_app_key_secret(APP_KEY, APP_SECRET, REDIRECT_URL)
    token = oauth2.request_access_token(code);
    
    openid = token['openid']
    access_token = token['access_token']
    expires_in = token['expires_in']
    refresh_token = token['refresh_token']
    state = token['state']
    name = token['name']
    nick = token['nick']

    ACCESS_TOKEN = access_token
    OPENID = openid
    oauth2.set_access_token(ACCESS_TOKEN)
    oauth2.set_openid(OPENID)
    
    api = API(oauth2)
   
    # write to session
    req.session['user'] = {'nick':nick, 'name':name, 'openid':openid}
    #return HttpResponse(json.dumps(token), mimetype='text/json; charset=utf-8')
    return HttpResponseRedirect('/')
    
# GET 
def weibo_statuses_home_timeline(req):
    oauth2 = OAuth2Handler()
    oauth2.set_app_key_secret(APP_KEY, APP_SECRET, REDIRECT_URL)
    oauth2.set_access_token(ACCESS_TOKEN)
    oauth2.set_openid(OPENID)
    api = API(oauth2)
    
    return HttpResponse(json.dumps(api.get.statuses__home_timeline(format = 'json', pageflag = 0, pagetime = 0, reqnum = 50, type = 1, contenttype = 0)), mimetype='text/json; charset=utf-8')

def weibo_other_kownperson(req):
    oauth2 = OAuth2Handler()
    oauth2.set_app_key_secret(APP_KEY, APP_SECRET, REDIRECT_URL)
    oauth2.set_access_token(ACCESS_TOKEN)
    oauth2.set_openid(OPENID)
    api = API(oauth2)
    
    return HttpResponse(json.dumps(api.get.other__kownperson(format='json', reqnum=10, startindex=0)), mimetype='text/json; charset=utf-8')

#POST
def weibo_post(req):
    text = req.GET.get('text')
    url = req.GET.get('url')
    
    oauth2 = OAuth2Handler()
    oauth2.set_app_key_secret(APP_KEY, APP_SECRET, REDIRECT_URL)
    oauth2.set_access_token(ACCESS_TOKEN)
    oauth2.set_openid(OPENID)
    api = API(oauth2)
    if url:
        api.post.t__add_pic_url(content = text, pic_url=url)
    else:
        api.post.t__add(content = text)
    return HttpResponse(text)

def weibo_t_comment(req):
    text = req.GET.get('text');
    return HttpResponse(text)