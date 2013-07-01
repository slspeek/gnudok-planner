'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
import datetime
from .models import Calendar
from .models import TimeSlot, Car, Rule
import logging

# Very important, change made at june 26 2013
APPOINTMENTS_PER_HALF_DAY = 6


def get_region(calendar):
    """ Return the region for given calendar object, just for the heading """ 
    car = calendar.car
    timeslot = calendar.timeslot
    rule = Rule.objects.filter(timeslot=timeslot, car=car).all()[0]
    return rule.region


def get_total_weight(appointment_list):
    """ Returns the total weigth of the appointments is the given list """
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
        return APPOINTMENTS_PER_HALF_DAY
    else:
        entry = calendar_entries[0]
        appointment_list = entry.active_appointments().all()
        total_weight = get_total_weight(appointment_list)
        left = APPOINTMENTS_PER_HALF_DAY - total_weight
        return left


def _get_rules(date, region):
    """ Returns a list of rules for the given region on the given date. """
    week_day = date.weekday() + 1
    if region:
        rules = Rule.objects.filter(region=region,
                                    timeslot__day_of_week=week_day)
    else:
        rules = Rule.objects.filter(timeslot__day_of_week=week_day)
    return rules

def get_rules(date, regions):
    result = []
    if regions == None:
        rules = _get_rules(date, None)
        for rule in rules:
             result.append(rule)
    else:
        for region in regions:
            rules = _get_rules(date, region)
            for rule in rules:
                result.append(rule)
    return result
 
def get_free_entries_new(fromDate, daysAhead, regions, min_weight):
    result = []
    for offset in range(0, 60):
        date = fromDate + datetime.timedelta(days=offset)
        rules = get_rules(date, regions)
        for rule in rules:
            free_count = get_free_count(date, rule)
            if free_count >= min_weight:
                result.append(entry(date, rule))
        if len(result) >= 2 and offset >= daysAhead - 1:
            break
    return result


def get_free_entries_with_extra_calendar(fromDate,
                                         daysAhead,
                                         regions,
                                         min_weight,
                                         calendar):
    result = get_free_entries_new(fromDate, daysAhead, regions, min_weight)
    found = False
    for entry in result:
        if entry[0] == calendar.pk:
            found = True
    if not found:
        result = [(calendar.pk, str(calendar))] + result
    return result


def entry(date, rule):
    timeslot_id = rule.timeslot.pk
    car_id = rule.car.pk
    calendar = get_or_create_calendar(timeslot_id, car_id, date)
    return (calendar.pk, str(calendar))


def get_or_create_calendar(timeslot_id, car_id, date):
    """ Returns exiting calendar object for this triplet or creates one
    if non-existent"""
    by_date = Calendar.objects.filter(date=date)
    calendars = by_date.filter(timeslot__pk=timeslot_id).filter(car__pk=car_id)
    if calendars:
        calendar = calendars[0]
    else:
        calendar = Calendar()
        calendar.date = date
        calendar.timeslot = TimeSlot.objects.get(pk=int(timeslot_id))
        calendar.car = Car.objects.get(pk=int(car_id))
        calendar.save()
    return calendar
