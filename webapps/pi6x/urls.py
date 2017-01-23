#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'c8d8z8@gmail.com'

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import pi6x.views
#import jquery_plugins_demo.views

urlpatterns = [
    # Examples:
    #url(r'^hello/$', pi6x.views.hello),
    # app-polls
    #url(r'^polls/', include('polls.urls', namespace='polls')),

    # account manage page
    #url('^app_list$', pi6x.views.app_list),
    #url('^auth/'),

    # jquery plugins demo
    #url(r'jquery_plugins_demo',)

    # 程序入口 的 登陆
    url(r'^$', pi6x.views.index),
    #url(r'^login$',pi6x.views.login),
    #url(r'^logout$',signout),

    # import apps urls
    url(r'^solr/', include('searchbysolr_app.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^weibo/', include('weibo.urls')),

    #url(r'^hello/$', hello),
    # api
    #url('^api/auth/login$', auth_login),
    #url('^api/auth/callback$', auth_callback),
    #url('^api/weibo/home$', weibo_statuses_home_timeline),
    #url('^api/weibo/other/kownperson$', weibo_other_kownperson),
    #url('^api/weibo/post$', weibo_post),

    url(r'^sysctl$',pi6x.views.sysctl),
    url(r'^api/tomcat_status.json$',pi6x.views.monitor_tomcat)

  ]
#print urlpatterns
urlpatterns += staticfiles_urlpatterns()
#print urlpatterns
