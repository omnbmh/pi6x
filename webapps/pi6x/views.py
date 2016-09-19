
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template
from django.template import loader

import os
import datetime

def login(req):
    t = get_template('login.html')
    c = template.Context({})
    return HttpResponse(t.render(c))

def index(req):
    if 'user' in req.session:
        context = {'is_login':True, 'uid':req.session['user']['uid'], 'name':req.session['user']['name']}
    else:
        context = {'is_login':'false'}

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, req))

def app_list(req):
    t = get_template('app_list_tab.html')
    c = template.Context({})
    return HttpResponse(t.render(c))

def hello(req):
    return HttpResponse("<h1>Welcome To Pi World!</h1>");

def homepage(req):
    return HttpResponse('hello gays');

def sysctl(req):
    t = get_template('sysctl.html')
    i = os.popen('systeminfo').readline()
    c = template.Context({"info":i})
    return HttpResponse(t.render(c))
