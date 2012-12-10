'''
Admin configuration
'''
from __future__ import absolute_import
from .models import Customer,  TimeSlot, Appointment, Calendar, Region, Car, Rule
from django.contrib import admin

class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    
class AppointmentInline(admin.TabularInline):
    model = Appointment

class CalendarAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    
    inlines = [AppointmentInline,]
    
class AppointmentAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(TimeSlot)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Region)
admin.site.register(Rule)
admin.site.register(Car)
