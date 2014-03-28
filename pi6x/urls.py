from django.conf.urls import patterns, include, url
from django.contrib import admin
import pi6x.views

from weibo.view import hello, home, signin, signout, ctime, send
from weibo.api import auth_login, auth_callback, weibo_statuses_home_timeline, weibo_other_kownperson, weibo_post

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'firstsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    # account manage page 
    url('^$', pi6x.views.index),
    #url('^auth/'),
    
    
    
    
    
    
    
    #url('^signin$',pi6x.views.index),
    #url('^signout$',signout),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weibo/', include(weibo.urls)),
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
)
