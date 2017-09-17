from django.conf.urls import url

from . import views

app_name = 'notes'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^new/$', views.new_note, name='new_note'),
    url(r'^note/(?P<pk>[0-9]+)/edit/$', views.edit_note, name='edit_note'),
    url(r'^note/(?P<pk>[0-9]+)/delete/$', views.delete_note, name='delete_note')
]
