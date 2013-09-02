from django.conf.urls import patterns, include, url
from . import views
import chat
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from groups import views as group_views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'galcon.views.home', name='home'),
    # url(r'^galcon/', include('galcon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
    (r"^$", views.home),
    ("^games/$", views.games),
    ("^igalcon/$", views.igalcon),
    ("^fusion/$", views.fusion),
    ("^support/$", views.support),
    ("^login/", views.login),
    ("^logout/$", views.logout),
    ("^register/", views.register),
    (r"^users/(\w+)/$", views.profile),
    (r"^users/(\w+)/friends/$", views.friends),
    (r"^users/(\w+)/edit/$", views.edit_profile),
    (r"^users/(?P<username>\w+)/highest_flag/", views.highest_flag),
    (r"^users/(?P<username>\w+)/groups/$", group_views.groups),
    
    ("^forums/", include("forums.urls")),
    ("^groups/", include("groups.urls")),
    ("^chat/", include("chat.urls")),
    ("^messages/", include("messaging.urls")),
)

if settings.DEBUG:
    urlpatterns += patterns('', (r'^site/(?P<path>.*)$', 'django.views.static.serve',
                                 {'document_root': settings.STATIC_ROOT}),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
