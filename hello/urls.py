from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^findbymonth/$', views.findbymonth),
    url(r'^home/$', views.home),
    url(r'^error/$', views.error),
    url(r'^login/$', views.login),
    url(r'^book/$', views.book),
]
