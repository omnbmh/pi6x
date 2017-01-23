#!/usr/bin/python
# -*- coding: utf-8 -*-
# 依赖 httpmylib

__author__ = 'omnbmh(c8d8z8@gmail.com)'

import httpmylib

class SolrClient():
    def __init__(self,url):
        # http://10.100.142.94:8081/solr/orgams_log_core/select?q=*%3A*&wt=json&indent=true
        self.update_url = url+'/update/'
        self.select_url = url + '/select/'
        self.docs =[];
        self.size = 0;

    def select(self,query_dict):
        res = httpmylib.GET(self.select_url,query_dict);
        return res

    def delAll(self):
        pass

if __name__ == '__main__':
    solrcli = SolrClient('http://10.100.142.94:8081/solr/orgams_log_core')

    query_dict = {}
    query_dict['q']= 'ctime:*'
    query_dict['wt'] = 'json'
    query_dict['indent'] = 'true'
    solrcli.select(query_dict)
