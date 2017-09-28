from django.conf.urls import url
from . import views

app_name = 'todo'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new/$', views.new_project, name='new_project'),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', views.edit_project, name='edit_project'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.delete_project, name='delete_project'),
    url(r'^task/(?P<pk>[0-9]+)/$', views.new_task, name='new_task'),
    url(r'^task/(?P<pk>[0-9]+)/(?P<tk>[0-9]+)/edit/$', views.edit_task, name='edit_task'),
    url(r'^task/(?P<pk>[0-9]+)/(?P<tk>[0-9]+)/delete/$', views.delete_task, name='delete_task'),
    url(r'^subtask/(?P<pk>[0-9]+)/(?P<tk>[0-9]+)/$', views.new_subtask, name='new_subtask'),
    url(r'^subtask/(?P<pk>[0-9]+)/(?P<sk>[0-9]+)/edit/$', views.edit_subtask, name='edit_subtask'),
    url(r'^subtask/(?P<pk>[0-9]+)/(?P<sk>[0-9]+)/delete/$', views.delete_subtask, name='delete_subtask')
]