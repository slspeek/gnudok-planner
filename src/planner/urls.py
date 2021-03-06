""" Url configuration """
from __future__ import absolute_import
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import login
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from .main import urls
from .nlpostalcode import urls as postalcode_urls
from .main.views import logout_view
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^admin/doc/',
                        include('django.contrib.admindocs.urls')),
                       (r'^admin/',
                        include(admin.site.urls)),
                       url(r'^accounts/login/$',
                           login, name='Login'),
                       url(r'^accounts/logout/$', logout_view, name='Logout'),
                       (r'^main/', include(urls)),
                       (r'^pc/', include(postalcode_urls)),
                       url(r'^$', RedirectView.as_view(url='main/overview')),
                       )
urlpatterns += staticfiles_urlpatterns()
