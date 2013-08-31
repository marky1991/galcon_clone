from django.conf.urls import patterns
from . import views

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'galcon.views.home', name='home'),
    # url(r'^galcon/', include('galcon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    ("^$", views.join),
    ("^join/", views.join),
    ("^(?P<room_name>\w+)/join/$", views.join),
    ("^leave/$", views.leave),
    ("^post/$", views.post),
    ("^poll/$", views.poll),
    ("^(?P<room_name>\w+)/", views.main),
)
