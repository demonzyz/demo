from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^add_event/$', views.add_event),
<<<<<<< HEAD
    url(r'^get_eventlist/$', views.get_eventlist),
    url(r'^get_eventdetail/$', views.get_eventdetail),
    url(r'^set_status/$', views.set_status),
    url(r'^add_guest/$', views.add_guest),
    url(r'^get_guestlist/$', views.get_guestlist),
    url(r'^sign/$', views.sign),
    url(r'^register/$', views.register),



=======
    url(r'^get_eventlist$', views.get_eventlist),
    url(r'^get_eventdetail$', views.get_eventdetail),
    url(r'^set_status$', views.set_status),
    url(r'^add_guest$', views.add_guest),
    url(r'^get_guestlist$', views.get_guestlist),
>>>>>>> master
]
