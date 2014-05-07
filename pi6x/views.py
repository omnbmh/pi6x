from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template

import datetime

# Create your views here.
def index(req):
    t = get_template('index.html')
    c = template.Context({})
    return HttpResponse(t.render(c))
    
def app_list(req):
    t = get_template('app_list_tab.html')
    c = template.Context({})
    return HttpResponse(t.render(c))