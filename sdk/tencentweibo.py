# coding:utf-8
# author:Chen Dezhi
# version: 1.0

import time
import gzip
import urllib
import httplib
import collections
import mimetypes

import json
import StringIO

_DEBUG = False

if _DEBUG:
    import sys 
    reload(sys) 
    sys.setdefaultencoding('utf8')

class OAuth2Handler(object):
    def __init__(self, auth_url="https://open.t.qq.com/cgi-bin/oauth2/"):
        self.auth_url = auth_url
        self.app_key = None
        self.app_secret = None
        self.redirect_uri = None
        self.access_token = None
        self.expires = 0.0
        self.openid = None
        self.openkey = None

    def set_app_key_secret(self, app_key, app_secret, redirect_uri):
        self.app_key = str(app_key)
        self.app_secret = str(app_secret)
        self.redirect_uri = redirect_uri

    def set_access_token(self, access_token, expires_in=8035200):
        self.access_token = str(access_token)
        self.expires = int(time.time()) + float(expires_in)

    def set_openid(self, openid, openkey=None):
        self.openid = openid
        self.openkey = openkey

    def get_authorize_url(self):
        # https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=APP_KEY&response_type=code&redirect_uri=http://www.myurl.com/example
        return "%sauthorize?client_id=%s&response_type=%s&redirect_uri=%s" % (self.auth_url, self.app_key, "code", self.redirect_uri)
        
    def get_access_token_url(self, code):
        # https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=APP_KEY&client_secret=APP_SECRET&redirect_uri=http://www.myurl.com/example&grant_type=authorization_code&code=CODE
        return "%saccess_token?client_id=%s&client_secret=%s&redirect_uri=%s&grant_type=%s&code=%s" % (self.auth_url, self.app_key, self.app_secret, self.redirect_uri, "authorization_code", code)

    def request_access_token(self, code):
        #
        url = self.get_access_token_url(code)
        print url
        conn = httplib.HTTPSConnection("open.t.qq.com", timeout=60)
        conn.request("GET", url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) TencentWeiboPythonSDK", 'Accept-encoding':'gzip'})
        req = conn.getresponse()
        print req.status, req.reason
        data = req.read()
        parm = data.split('&')
        
        token = {}
        
        for kv in parm:
            key_val = kv.split('=')
            token[str(key_val[0])] = key_val[1]
        
        return token
        
    def refresh_token_url(self, refresh_token):
        # https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=APP_KEY&grant_type=refresh_token&refresh_token=REFRESH_TOKEN
        return "%saccess_token?client_id=%s&grant_type=refresh_token&refresh_token=%s" % (self.auth_url, self.app_key, refresh_token)

    def get_oauth_params(self, clientip="10.0.0.1"):
        """ return http param for string """
        if (self.app_key == None) or (self.access_token == None) or (self.openid == None):
            raise Exception("app_key(%s) or access_token(%s) or openid(%s) miss!" % (self.app_key, self.access_token, self.openid))

        oauth2_string = "oauth_consumer_key=%s&access_token=%s&openid=%s&clientip=%s&oauth_version=2.a&scope=all" \
            % (self.app_key, self.access_token, self.openid, clientip)
        return oauth2_string

    
class TWeiboError(Exception):
    """TWeibo API exception"""

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
    args = []
    for k, v in kw.iteritems():
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            args.append('%s=%s' % (k, urllib.quote(qv)))
        elif isinstance(v, collections.Iterable):
            for i in v:
                qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                args.append('%s=%s' % (k, urllib.quote(qv)))
        else:
            qv = str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(str(arg) for arg in args)

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

    # Connect to host
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
        conn.request(method, http_url, headers=req_headers, body=http_body)
        resp = conn.getresponse()
    except Exception, e:
        raise TWeiboError('Failed to send request: %s' % (e))

    if resp.status != 200:
        raise TWeiboError("[HTTP %s] %s" % (resp.status, resp.read()))

    # Parse the response payload
    body = resp.read()
    if resp.getheader('Content-Encoding', '') == 'gzip':
        try:
            zipper = gzip.GzipFile(fileobj=StringIO.StringIO(body))
            body = zipper.read()
        except Exception, e:
            raise TWeiboError('Failed to decompress data: %s' % e)

    if _DEBUG:
        print "(%s) [DEBUG] %s" % (time.time(), body)

    # raise TWeiboError(body) when API return None
    try:
        result = _parse_json(body)
    except Exception, e:
        raise TWeiboError("parse_json() error: %s" % (e), body=body)

    # check errcode
    if hasattr(result, 'errcode'):
        if int(result.errcode) != 0:
            raise TWeiboError("[ERROR] errcode=%s, ret=%s, msg:%s\n\n%s" % (result.errcode, result.ret, result.msg, body), body=body, result=result)

    if _DEBUG:
        print "(%s) [DEBUG] errcode=%s, ret=%s, msg:%s" % (time.time(), result.errcode, result.ret, result.msg)

    conn.close()
    return result


class HttpObject(object):

    def __init__(self, api, method):
        self.api = api
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            return _http_call(self.api, '%s%s' % (self.api.api_url, attr.replace('__', '/')), self.method, **kw)
        return wrap

class API(object):
    """Tencent Weibo API for Python"""
    def __init__(self, auth, host="open.t.qq.com", port=80, compression=True, timeout=60, headers=None):
        self.auth = auth
        self.host = host
        self.port = port
        self.compression = compression
        self.timeout = timeout
        self.api_url = "https://open.t.qq.com/api/"
        self.headers = headers or {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) TWeiboPySDK",
            }
        self.get = HttpObject(self, "GET")
        self.post = HttpObject(self, "POST")
        self.upload = HttpObject(self, "UPLOAD")

        if (not self.auth):
            raise Exception("Authentication required! See wiki OAuth2Handler() for help.")
