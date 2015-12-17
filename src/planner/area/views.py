from __future__ import absolute_import
from planner.main.models import Region

def get_regions_for_postcalcode(postalcode):
    postalcode = postalcode.lower()
    regions = Region.objects.filter(interval__begin__lte=postalcode, interval__end__gte=postalcode)
    return  set(regions)
