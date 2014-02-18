from __future__ import absolute_import
from planner.main.models import Region
import logging

def get_regions_for_postcalcode(postalcode):
    postalcode = postalcode.lower()
    regions = Region.objects.filter(interval__begin__lte=postalcode, interval__end__gte=postalcode)
    #logging.info("SQL: %s" % regions.query.__str__())
    return  set(regions)
    
