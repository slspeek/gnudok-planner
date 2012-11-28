'''
Admin configuration
'''
from __future__ import absolute_import
from .models import Customer,  TimeSlot, Appointment, Calendar, Region
from django.contrib import admin

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
admin.site.register(Calendar)
admin.site.register(Region)
