from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns(
    "",
    ("^$", views.Inbox.as_view()),
    ("^(?P<message_id>\d+)/$", views.Message.as_view()),

    ("^new/$", views.Modify_Message.as_view()),
    (r"^inbox/((?P<page_number>\d*)/)?$", views.Inbox.as_view()),
    ("^starred/((?P<page_number>\d*)/)?$", views.Starred_Messages.as_view()),
    ("^sent/((?P<page_number>\d*)/)?$", views.Sent_Messages.as_view()),
    ("^drafts/((?P<page_number>\d*)/)?$", views.Drafts.as_view()),
    ("^trash/((?P<page_number>\d*)/)?$", views.Trash.as_view()),
    )
