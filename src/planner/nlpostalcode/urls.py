from __future__ import absolute_import
from django.conf.urls import patterns
from planner.nlpostalcode.views import get_info_on_postalcode

urlpatterns = patterns(
    '',
    (r'^get/(?P<postalcode>\w+)', get_info_on_postalcode),
)
