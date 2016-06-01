#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'c8d8z8@gmail.com'
"""pi6x URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

#import event54.views
#import event.views
import pi6x.views
#import jquery_plugins_demo.views
#admin.autodiscover()

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
    #url(r'^$', 'pi6x.views.index', name='index'),
    #url(r'^login$',pi6x.views.login),
    #url(r'^logout$',signout),
    
    # import apps urls
    #url(r'^solr/', include('searchbysolr_app.urls')),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^weibo/', include('weibo.urls')),
    #url(r'^event54/$', event54.views.index),
    #url(r'^event54/authorize', event54.views.authorize),
    #event
    #url(r'^event/$', event.views.index),
    #url(r'^event/create$', event.views.create),
    
    #url(r'^hello/$', hello),
    #url(r'^time/$', 'firstsite.view.current_datetime', name='current_datetime'),
    #url(r'^time/(\d{1,2})/$', ctime),
    #url(r'^time/plus/(\d{1,2})/$','firstsite.view.hours_add', name='time-plus'), 
    #url(r'^person/$','firstsite.view.person', name='person'), 
    #url(r'^.*$', 'firstsite.view.error', name='error'),
    
    # api
    #url('^api/auth/login$', auth_login),
    #url('^api/auth/callback$', auth_callback),
    #url('^api/weibo/home$', weibo_statuses_home_timeline),
    #url('^api/weibo/other/kownperson$', weibo_other_kownperson),
    #url('^api/weibo/post$', weibo_post),
    
    url(r'^sysctl$',pi6x.views.sysctl),
    
  ]
