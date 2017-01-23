#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.template import loader

import commonlib.httpmylib
import commonlib.solrlib

import json
# Create your views here.
def index(req):
    template = loader.get_template('searchbysolr/index.html')
    context = {}
    return HttpResponse(template.render(context, req))

def search(req):
    key = ''
    # request solr result
    template = loader.get_template('searchbysolr/index.html')
    context = {}
    return HttpResponse(template.render(context, req))

'''
以下是api接口
'''
def query(req):
    q = req.GET.get('q_text');
    if not q:
        q = ''

    solrcli = commonlib.solrlib.SolrClient('http://10.100.142.94:8081/solr/orgams_log_core')

    query_dict = {}
    query_dict['q']= 'info:*'+q+'*'
    query_dict['wt'] = 'json'
    query_dict['indent'] = 'true'
    print 123
    resp = solrcli.select(query_dict)
    return HttpResponse(json.dumps(resp));
