# Create your views here.
from __future__ import absolute_import
from .models import Street
from django.http import HttpResponse
from django.utils import simplejson
import logging

def get_info_on_postalcode(request, postalcode):
    pc_code = int(postalcode[0:4])
    pc_chars = postalcode[4:6]    
    streets  = Street.objects.filter(postcode__fourpp=pc_code).filter(chars=pc_chars)
    street = streets[0]
    town = street.postcode.city.cityname_set.all()[0].name
    address = street.street
    data = {'address': address, 'town': town}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')