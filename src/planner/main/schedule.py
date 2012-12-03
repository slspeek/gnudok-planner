'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
import datetime
from .models import Calendar
from .models import TimeSlot, Car, Rule

def get_total_weight(appointment_list):
    weight = 0
    for app in appointment_list:
        weight += app.weight
    return weight
    

def get_free_count(date, rule):
    """ Given a date, timeslot and region return the number of free slots """
    query = Calendar.objects.filter(date=date)
    query = query.filter(timeslot=rule.timeslot)
    query = query.filter(car=rule.car)
    calendar_entries = query.all()
    if not calendar_entries:
        return 4
    else:
        entry = calendar_entries[0]
        appointment_list = entry.appointment_set.all()
        total_weight = get_total_weight(appointment_list)  
        left = 4 - total_weight
        return left


def get_rules(date, region):
    """ Returns a list of timeslots for the given region on the given date. """
    week_day = date.weekday() + 1
    
    rules = Rule.objects.filter(region=region,timeslot__day_of_week=week_day)
    return rules


def get_free_entries(fromDate, daysAhead, region, min_weight):
    """ Return a list of triplet containing date,
     rule and number of free slots.
     A triplet with no free slots is left out. """
    result = []
    for offset in range(0, 60):
        date = fromDate + datetime.timedelta(days=offset)
        rules = get_rules(date, region)
        for rule in rules:
            free_count = get_free_count(date, rule)
            if free_count >= min_weight:
                result.append((date, rule, free_count))
        if len(result) >= 2 and offset >= daysAhead - 1:
            break;
    return result


def get_or_create_calendar(timeslot_id, car_id, date):
    """ Return exiting calendar object for this triplet or creates one 
    if non-existent"""
    calendars = Calendar.objects.filter(date=date).filter(timeslot__pk=timeslot_id).filter(car__pk=car_id)
    if calendars:
        calendar = calendars[0]
    else:
        calendar = Calendar()
        calendar.date = date
        calendar.timeslot = TimeSlot.objects.get(pk=int(timeslot_id))
        calendar.car = Car.objects.get(pk=int(car_id))
        calendar.save()
    return calendar

