from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    "",
    (r"^$", views.groups),
    (r"^(?P<action>new)/$", views.modify_group),
    #IF there's a page number, we match on this. (/groups/newest/1/ would match
    #here)
    ("^(?P<sorting_function>\w+)/(?P<page_number>\d+)/", views.groups),
    ("^(?P<sorting_function>(newest|oldest|biggest|smallest))/$", views.groups),
    ("^(?P<group_name>[\w\.]+)/$", views.group),
    ("^(?P<group_name>[\w\.]+)/(?P<kind>requests)/$", views.requests),
    ("^(?P<group_name>[\w\.]+)/(?P<kind>blocks)/$", views.requests),
    ("^(?P<group_name>[\w\.]+)/(?P<action>edit)/$", views.modify_group),
    ("^(?P<group_name>[\w\.]+)/(?P<action>join)/$", views.change_membership),
    ("^(?P<group_name>[\w\.]+)/(?P<action>leave)/$", views.change_membership),
    ("^(?P<group_name>[\w\.]+)/admins/$", views.change_adminship)
)
