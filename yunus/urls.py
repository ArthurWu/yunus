from django.conf.urls import patterns, include, url
from django.contrib import admin
from feed import LatestArticleFeed
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'yunus.views.home', name='home'),
    url(r'^search$', 'yunus.views.search', name='search'),
    url(r'^subscibe$', 'yunus.views.subscibe', name='subscibe'),
    url(r'^about-us$', 'yunus.views.about_us', name='about_us'),
    url(r'^contact-us$', 'yunus.views.contact_us', name='contact_us'),
    url(r'^send_emails/$', 'yunus.views.send_emails', name='send_emails'),
    url(r'^change_language/$', 'yunus.views.change_language', name='change_language'),
    url(r'^menu/(\d+)$', 'yunus.views.menu'),
    url(r'^menu/(\d+)/(\d+)$', 'yunus.views.sub_menu'),
    url(r'^centre/', include('centre.urls')),

    url(r'^latest/feed/$', LatestArticleFeed()),

    url(r'^admin/', include(admin.site.urls)),
)

import settings
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
        url(r'^media/(?P<path>.*)$', 'serve'),
    )
