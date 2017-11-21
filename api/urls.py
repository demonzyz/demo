from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^add_event/$', views.add_event),
    url(r'^get_eventlist$', views.get_eventlist),
]
