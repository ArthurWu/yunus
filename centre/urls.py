from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^articles$', 'centre.views.articles', name='articles'),
    url(r'^article/(\d+)$', 'centre.views.article', name='article'),
    url(r'^contact$', 'centre.views.contact', name='contact'),
)