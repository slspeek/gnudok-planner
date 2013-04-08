from __future__ import absolute_import
from .models import Interval
from django.http import HttpResponse


def get_region_for_postalcode_view(request, postalcode):
    region = get_regions_for_postcalcode(postalcode)
    return HttpResponse(str(region))


def get_region_for_postcalcode(postalcode):
    matching_intervals = Interval.objects.filter(begin__lte=postalcode,
                                                 end__gte=postalcode)
    if matching_intervals:
        interval = matching_intervals[0]
        return interval.region
    else:
        return 'Unknown'
    
def get_regions_for_postcalcode(postalcode):
    matching_intervals = Interval.objects.filter(begin__lte=postalcode,
                                                 end__gte=postalcode)
    return map(lambda x: x.region, matching_intervals) 