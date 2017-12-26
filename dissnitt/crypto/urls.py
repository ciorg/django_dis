from django.conf.urls import url

from . import views

app_name = 'crypto'

urlpatterns = [
    url('', views.index, name='index'),
]