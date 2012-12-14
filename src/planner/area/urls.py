from __future__ import absolute_import
from .views import get_region_for_postalcode_view
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^postalcode/(?P<postalcode>\d{4}\w{2})$', get_region_for_postalcode_view, name='Postalcode2Region'),
   
)
