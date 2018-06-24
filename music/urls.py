from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = "music"

urlpatterns = [
    #/music/
    url(r'^$',views.IndexView.as_view(),name="index"),
    #/music/<album_id>/
    url(r'^(?P<pk>[0-9]+)/$',views.detail,name="detail"),
    #/music/<album_id>/favorite/
    url(r'^(?P<pk>[0-9]+)/favorite/$', views.favorite, name="favorite"),
    #/music/album/add/
    url(r'^album/add/$',views.AlbumCreate.as_view(),name='album-add'),
    # /music/album/update/
    url(r'^album/(?P<pk>[0-9]+)/$', views.AlbumUpdate.as_view(), name='album-update'),
    #/music/album/delete/
    url(r'^album/(?P<pk>[0-9]+)/delete/$',views.AlbumDelete.as_view(),name='album-delete'),
    #/music/register/
    url(r'^register/$',views.UserFormView.as_view(),name='register'),

]
