from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name='mylogin'

urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'mylogin/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/mylogin/login'}, name='logout'),
    url(r'^home/$', views.home, name='home')
]