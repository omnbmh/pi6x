from django.conf.urls import patterns, include, url
from django.contrib import admin

from weibo.view import hello, home, signin, signout, ctime, send
from weibo.api import auth_login, auth_callback, weibo_statuses_home_timeline, weibo_other_kownperson, weibo_post

admin.autodiscover()

urlpatterns = patterns('',
    url('^api/auth/login$', auth_login),
    url('^api/auth/callback$', auth_callback),
    url('^api/weibo/home$', weibo_statuses_home_timeline),
    url('^api/weibo/other/kownperson$', weibo_other_kownperson),
    url('^api/weibo/post$', weibo_post),
)
