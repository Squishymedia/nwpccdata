from django.conf.urls import patterns, include, url
from rest_framework import routers
from django.contrib import admin
from data import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'data.views.index', name='index'),
    url(r'^sets/?$', views.DataSetViewSet.as_view({'get': 'list'})),
    url(r'^sets/(?P<id>\d+)/?$', views.DataSetViewSet.as_view({'get': 'detail'})),
    url(r'^sets/(?P<id>\d+)/(?P<revision>\d)/?$', views.DataSetRevisionViewSet.as_view({'get': 'detail'})),
    url(r'^sets/(?P<id>\d+)/current/?$', views.DataSetRevisionViewSet.as_view({'get': 'current'})),
    url(r'^sets/(?P<id>\d+)/latest/?$', views.DataSetRevisionViewSet.as_view({'get': 'latest'})),
    url(r'^sets/(?P<id>\d+)/(?P<revision>\d)/approve/?$', 'data.views.approve_set_data', name='approve_set'),
    url(r'^sets/(?P<id>\d+)/new_xls/?$', 'data.views.post_new_xls', name='new_xls'),
    url(r'^tests/?$', 'data.views.tests', name='tests'),
    url(r'^admin/?', include(admin.site.urls)),
)
