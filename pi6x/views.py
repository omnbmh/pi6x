from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template

import datetime

# Create your views here.
def index(req):
    #if 'user' in req.session:
    #    t = get_template('index.html')
    #    c = template.Context({})
    #else:
    #    t = get_template('page/signin.html')
    #    c = template.Context({})
    t = get_template('index.html')
    c = template.Context({})
    return HttpResponse(t.render(c))
    
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
    c = template.Context({})
    return HttpResponse(t.render(c))