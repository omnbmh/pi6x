from django.conf.urls import url

from views import hello, home, signin, signout, ctime, send
from api import auth_login, auth_callback, weibo_statuses_home_timeline, weibo_other_kownperson, weibo_post

urlpatterns = [
    url('^api/auth/login$', auth_login),
    url('^api/auth/callback$', auth_callback),
    url('^api/weibo/home$', weibo_statuses_home_timeline),
    url('^api/weibo/other/kownperson$', weibo_other_kownperson),
    url('^api/weibo/post$', weibo_post),
]
