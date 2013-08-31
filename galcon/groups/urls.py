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
    (r"^(?P<group_name>\w+)/$", views.group),
    (r"^(?P<group_name>\w+)/(?P<kind>requests)/$", views.requests),
    (r"^(?P<group_name>\w+)/(?P<kind>blocks)/$", views.requests),
    (r"^(?P<group_name>\w+)/(?P<action>edit)/$", views.modify_group),
    (r"^(?P<group_name>\w+)/(?P<action>join)/$", views.change_membership),
    (r"^(?P<group_name>\w+)/(?P<action>leave)/$", views.change_membership),
    (r"^(?P<group_name>\w+)/admins/$", views.change_adminship)
)
