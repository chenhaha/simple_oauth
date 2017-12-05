from django.conf.urls import url
from . import  views

urlpatterns = [
    url(r'^authorize/$', views.authorize),
    url(r'^access_token/$', views.access_token),
    url(r'^client/$', views.client),
]
