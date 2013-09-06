from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    "",

    ("^$", views.Forums.as_view()),
    ("^(?P<url>[\w\.]+/)$", views.Forums.as_view()),
    ("^(?P<url>[\w\.]+/recent_posts/)$", views.Recent_Posts.as_view()),
    ("^(?P<url>[\w\.]+/[\w\.]+/)$", views.Forums.as_view()),
    ("^(?P<url>[\w\.]+/[\w\.]+/\d+/)$", views.Forums.as_view()),
    ("^(?P<url>[\w\.]+/[\w\.]+/\d+/\d+/)$", views.Forums.as_view()),
    ("^(?P<url>[\w\.]+/\d+/\d+/)(?P<action>edit)/$", views.Modify_Post.as_view()),
    ("^(?P<url>[\w\.]+/[\w\.]+/\d+/\d+/)(?P<action>reply)/$", views.Modify_Post.as_view()),
    ("^(?P<url>[\w\.]+/[\w\.]+/)new_thread/$", views.Create_Thread.as_view()),
    )
