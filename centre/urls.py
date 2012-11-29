from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^article/(\d+)/$', 'centre.views.article', name='article'),
)