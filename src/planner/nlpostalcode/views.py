""" Views fro dutch postalcodes """
from __future__ import absolute_import
from .models import Street
from django.http import HttpResponse
import json

def get_streets(fourpp, chars):
    return Street.objects.filter(postcode__fourpp=fourpp).filter(chars=chars).all()

def get_info_on_postalcode(request, postalcode):
    """ Returns street and town for a complete postalcode """
    fourpp = int(postalcode[0:4])
    chars = postalcode[4:6]    
    streets  = get_streets(fourpp, chars)
    if streets:
        street = streets[0]
        town = street.postcode.city.get_official_name()
        address = street.street
        data = {'found': True, 'address': address, 'town': town}
    else:
        data = {'found': False }
    j = json.dumps(data)
    return HttpResponse(j, content_type='application/json')

def update(fourpp, chars, street_name):
    pass
