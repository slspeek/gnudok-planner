""" Views fro dutch postalcodes """
from __future__ import absolute_import
from .models import Street
from django.http import HttpResponse
from django.utils import simplejson

def get_streets(fourpp, chars):
    return Street.objects.filter(postcode__fourpp=fourpp).filter(chars=chars)

def get_info_on_postalcode(request, postalcode):
    """ Returns street and town for a complete postalcode """
    fourpp = int(postalcode[0:4])
    chars = postalcode[4:6]    
    streets  = get_streets(fourpp, chars)
    street = streets[0]
    town = street.postcode.city.cityname_set.all()[0]
    address = street.street
    data = {'address': address, 'town': town}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')

def update(fourpp, chars, street_name):
    pass