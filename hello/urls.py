from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^findbymonth/$', views.findbymonth),
    url(r'^login/$', views.login),
]
