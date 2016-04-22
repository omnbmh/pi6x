from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /solr/
    url(r'^$', views.index, name='index'),
]