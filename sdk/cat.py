#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import time
import gzip
import urllib
import httplib
import collections
import mimetypes

import json
import StringIO

class APIError(Exception):
    """API exception"""

    def __init__(self, reason, body=None, result=None):
        self.reason = unicode(reason)
        self.body = body
        self.result = result
        Exception.__init__(self, reason)

    def __str__(self):
        return self.reason

class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

def _parse_json(s):
    """parse str into JsonDict"""

    def _obj_hook(pairs):
        """convert json object to python object"""
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o

    return json.loads(s, object_hook=_obj_hook)

def _encode_params(**kw):
    '''
    Do url-encode parameters

    >>> _encode_params(a=1, b='R&D')
    'a=1&b=R%26D'
    >>> _encode_params(a=u'\u4e2d\u6587', b=['A', 'B', 123])
    'a=%E4%B8%AD%E6%96%87&b=A&b=B&b=123'
    '''
    def _encode(L, k, v):
        if isinstance(v, unicode):
            print '%s is unicode, value is %s, after utf-8 is %s.' % (k, v, v.encode('utf-8'))
            L.append('%s=%s' % (k, urllib.quote(v.encode('utf-8'))))
        elif isinstance(v, str):
            print '%s is str, value is %s, after utf-8 is %s.' % (k, v, v.encode('utf-8'))
            L.append('%s=%s' % (k, urllib.quote(v)))
        elif isinstance(v, collections.Iterable):
            for x in v:
                _encode(L, k, x)
        else:
            print '%s is other, value is %s.' % (k, v)
            L.append('%s=%s' % (k, urllib.quote(str(v))))
    args = []
    for k, v in kw.iteritems():
        _encode(args, k, v)
    return '&'.join(args)
    
def _guess_content_type(url):
    n = url.rfind('.')
    if n==(-1):
        return 'application/octet-stream'
    ext = url[n:]
    return mimetypes.types_map.get(ext, 'application/octet-stream')

def _encode_multipart(**kw):
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            filename = getattr(v, 'name', '')
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(filename))
            data.append(content)
            try:
                v.close()      # try close file obj
            except:
                pass
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(str(arg) for arg in data), boundary

def _http_call(api, url, method, **kw):
    boundary = None
    if (method == "GET"):
        params = _encode_params(**kw)
        http_url = "%s?%s&%s" % (url, params, api.auth.get_oauth_params())
        print http_url
        http_body = None
    elif (method == "UPLOAD"):
        method = "POST"
        params, boundary = _encode_multipart(**kw)
        http_url = "%s?%s" % (url, api.auth.get_oauth_params())
        http_body = params
    else: # if (method == "POST"):
        params = _encode_params(**kw)
        http_url = "%s?%s" % (url, api.auth.get_oauth_params())
        http_body = params
        print params
    # Connect to host
    if api.https:
        conn = httplib.HTTPSConnection(api.host, api.port, timeout=api.timeout)
    else:
        conn = httplib.HTTPConnection(api.host, api.port, timeout=api.timeout)

    # copy request header from api.headers
    #req_headers = { k:v for k,v in api.headers.iteritems() }
    # Fix python 2.6 'SyntaxError: invalid syntax' BUG
    req_headers = {}
    for k,v in api.headers.iteritems():
        req_headers[str(k)] = v

    # Request compression if configured
    if api.compression:
        req_headers['Accept-encoding'] = 'gzip'
    if boundary:
        req_headers['Content-Type'] = 'multipart/form-data; boundary=%s' % boundary

    # Execute request
    try:
        print req_headers
        print http_url
        conn.request(method, http_url, headers=req_headers, body=http_body)
        resp = conn.getresponse()
    except Exception, e:
        raise APIError('Failed to send request: %s' % (e))

    if resp.status != 200:
        raise APIError("[HTTP %s] %s" % (resp.status, resp.read()))

    # Parse the response payload
    body = resp.read()
    if resp.getheader('Content-Encoding', '') == 'gzip':
        try:
            zipper = gzip.GzipFile(fileobj=StringIO.StringIO(body))
            body = zipper.read()
        except Exception, e:
            raise APIError('Failed to decompress data: %s' % e)

    # raise APIError(body) when API return None
    try:
        result = _parse_json(body)
    except Exception, e:
        raise APIError("parse_json() error: %s" % (e), body=body)

    # check errcode
    if hasattr(result, 'errcode'):
        if int(result.errcode) != 0:
            raise APIError("[ERROR] errcode=%s, ret=%s, msg:%s\n\n%s" % (result.errcode, result.ret, result.msg, body), body=body, result=result)

    conn.close()
    return result


class HttpObject(object):

    def __init__(self, api, method):
        self.api = api
        self.method = method

    def call(self, url):
        def wrap(**kw):
            print '%s%s' % (self.api.api_url, url)
            return _http_call(self.api, '%s%s' % (self.api.api_url, url), self.method, **kw)
        return wrap
