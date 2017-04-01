from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template
from django.template import loader

# Create your views here.
def index(req):
    if 'user' in req.session:
        context = {'is_login':True, 'uid':req.session['user']['uid'], 'name':req.session['user']['name']}
    else:
        context = {'is_login':False}

    template = loader.get_template('jquery_plugins_demo/index.html')
    return HttpResponse(template.render(context, req))
