from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template

import zqb-unump
# Create your views here.
def unump(req):
    t = get_template('zqb-unump.html')
    c = template.Context({})
    return HttpResponse(t.render(c))
    
def unumpjson(req):
    zqb-unump.unump(phone)