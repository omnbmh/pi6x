#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
