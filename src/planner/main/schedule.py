'''
Created on 29 nov. 2012

@author: steven
'''
from __future__ import absolute_import
import datetime
from .models import Calendar, Appointment
from .models import TimeSlot, Car, Rule
import logging

# Very important, change made at june 26 2013
APPOINTMENTS_PER_HALF_DAY = 4

DELIVERY_PER_HALF_DAY = 2


def get_limit(kind): 
    if kind == Appointment.KIND_PICKUP: 
        return APPOINTMENTS_PER_HALF_DAY
    else:
        return DELIVERY_PER_HALF_DAY
        

def get_region(calendar):
    """ Return the region for given calendar object, just for the heading """ 
    car = calendar.car
    timeslot = calendar.timeslot
    rule = Rule.objects.filter(timeslot=timeslot, car=car).all()[0]
    return rule.region


def get_total_weight(appointment_list, kind=Appointment.KIND_DELIVERY):
    """ Returns the total weigth of the appointments in the given list of given kind """
    weight = 0
    apps_of_given_kind = filter(lambda x: x.kind == kind, appointment_list)
    for app in apps_of_given_kind:
        weight += app.weight
    return weight


def get_free_count(date, rule, kind=Appointment.KIND_DELIVERY):
    """ Given a date, timeslot and region return the number of free slots """
    query = Calendar.objects.filter(date=date)
    query = query.filter(timeslot=rule.timeslot)
    query = query.filter(car=rule.car)
    calendar_entries = query.all()
    if not calendar_entries:
        return get_limit(kind)
    else:
        entry = calendar_entries[0]
        appointment_list = entry.active_appointments().all()
        total_weight = get_total_weight(appointment_list, kind)
        left = get_limit(kind) - total_weight
        return left


def _get_rules(date, region, car_id):
    """ Returns a list of rules for the given region on the given date. """
    week_day = date.weekday() + 1
    if region:
        rules = Rule.objects.filter(region=region,
                                    timeslot__day_of_week=week_day)
    else:
        rules = Rule.objects.filter(timeslot__day_of_week=week_day)
        if car_id:
            rules = rules.filter(car__pk=car_id)
    return rules

def get_rules(date, regions, car_id):
    result = []
    if regions == None:
        rules = _get_rules(date, None, car_id)
        result.extend(rules)
    else:
        for region in regions:
            rules = _get_rules(date, region, car_id)
            result.extend(rules)
    return result


def _add_extra_calendar(entries, calendar):
    found = False
    for entry in entries:
        if entry[0] == calendar.pk:
            found = True
    if not found:
        entries = [(calendar.pk, str(calendar))] + entries
    return entries
 
def get_free_entries(fromDate, daysAhead, regions, min_weight, kind, car_id):
    result = []
    for offset in range(0, daysAhead):
        date = fromDate + datetime.timedelta(days=offset)
        rules = get_rules(date, regions, car_id)
        for rule in rules:
            free_count = get_free_count(date, rule, kind)
            if free_count >= min_weight:
                result.append(_entry(date, rule))
    return result


def get_free_entries_with_extra_calendar(fromDate,
                                         daysAhead,
                                         regions,
                                         min_weight,
                                         kind, car_id,
                                         calendar):
    entries = get_free_entries(fromDate, daysAhead, regions, min_weight, kind, car_id)
    return _add_extra_calendar(entries, calendar)


def _entry(date, rule):
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
