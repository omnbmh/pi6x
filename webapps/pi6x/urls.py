from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

import weibo.urls
from weibo.view import hello, home, signin, signout, ctime, send
from weibo.api import auth_login, auth_callback, weibo_statuses_home_timeline, weibo_other_kownperson, weibo_post
import event54.views
import event.views
import pi6x.views
import zanqianba_unump_app.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^hello/$', pi6x.views.hello),
    
    # url(r'^blog/', include('blog.urls')),
    
    # account manage page 
    url('^app_list$', pi6x.views.app_list),
    #url('^auth/'),
    
    
    
    
    
    # 程序入口 的 登陆
    url(r'^$', 'pi6x.views.index', name='index'),
    url(r'^login$',pi6x.views.login),
    url(r'^logout$',signout),
    
    
    
    
    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^weibo/', include(weibo.urls)),
    url(r'^event54/$', event54.views.index),
    url(r'^event54/authorize', event54.views.authorize),
    #event
    url(r'^event/$', event.views.index),
    url(r'^event/create$', event.views.create),
    
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
    
    
    #zanqianba_unump_app
    url(r'^zqbunump$',zanqianba_unump_app.views.unump),

)
