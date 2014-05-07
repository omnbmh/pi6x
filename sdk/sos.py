# -*- coding:utf-8 -*- #

import time
import gzip
import urllib
import httplib
import collections
import mimetypes

import json
import StringIO
from cat import HttpObject

class SosAPI(object):
    """sos API for Python"""
    def __init__(self, auth, host="127.0.0.1", port=8080, https=False, compression=True, timeout=60, headers=None):
        self.auth = auth
        self.host = host
        self.port = port
        self.https = https
        self.compression = compression
        self.timeout = timeout
        self.api_url = "http://127.0.0.1:8080/sos-api/"
        self.headers = headers or {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Python27",
            }
        self.get = HttpObject(self, "GET")
        self.post = HttpObject(self, "POST")
        self.upload = HttpObject(self, "UPLOAD")

        if (not self.auth):
            raise Exception("Authentication required! See wiki OAuth2Handler() for help.")

