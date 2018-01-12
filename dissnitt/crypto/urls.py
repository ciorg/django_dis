from django.conf.urls import url

from . import views

app_name = 'crypto'

urlpatterns = [
    url(r'^index', views.index, name='index'),
    url(r'^btc', views.btc, name='btc'),
    url(r'^eth', views.eth, name='eth')
]