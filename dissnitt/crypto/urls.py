from django.conf.urls import url

from . import views

app_name = 'crypto'

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^pdatag/(?P<table>[a-z]+)/$', views.pdatag, name='pdatag')
]