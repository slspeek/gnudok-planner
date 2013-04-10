from __future__ import absolute_import
from .models import Interval
from django.http import HttpResponse


def get_regions_for_postcalcode(postalcode):
    matching_intervals = Interval.objects.filter(begin__lte=postalcode,
                                                 end__gte=postalcode)
    return map(lambda x: x.region, matching_intervals) 