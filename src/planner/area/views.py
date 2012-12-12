from __future__ import absolute_import
from .models import Interval
from django.http import HttpResponse

def get_region_for_postalcode(request, postalcode):
    matching_intervals = Interval.objects.filter(begin__lte=postalcode, end__gte=postalcode)
    if matching_intervals:
        interval = matching_intervals[0]
        return HttpResponse(interval.region.name)
    else:
        return HttpResponse("Unknown")
