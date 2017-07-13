#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import template
from django.template.loader import get_template
from django.template import loader

import os
import datetime
import json

import commonlib.commonhttplib
# Create your views here.
def index(req):
    template = loader.get_template('flume_metrics/index.html')
    context = {}
    return HttpResponse(template.render(context, req))

'''
以下是api接口
'''
def capure_data(req):
    url = "http://10.100.32.48:41414/metrics";
    return HttpResponse(json.dumps(commonlib.commonhttplib.request(url)));
