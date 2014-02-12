'''
Admin configuration
'''
from __future__ import absolute_import
from .models import Customer, TimeSlot, \
    Appointment, Calendar, Region, Car, Rule
from planner.area.models import Interval
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'postcode', 'address', 'town',)
    search_fields = ['name']


class AppointmentInline(admin.TabularInline):
    model = Appointment


class CalendarAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    inlines = [AppointmentInline, ]


class AppointmentAdmin(admin.ModelAdmin):
    pass


class IntervalInline(admin.TabularInline):
    model = Interval


class RegionAdmin(admin.ModelAdmin):
    inlines = [IntervalInline, ]

class TimeSlotAdmin(admin.ModelAdmin):
    list_filter = ('day_of_week',)

class RuleAdmin(admin.ModelAdmin):
    list_filter = ('timeslot','car',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Car)
