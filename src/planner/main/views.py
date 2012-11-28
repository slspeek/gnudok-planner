# Create your views here.
from __future__ import absolute_import
import logging
import datetime
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import user_passes_test
from .models import Appointment, Region, TimeSlot, Calendar
from .forms import CalendarSearchForm, CustomerForm, AppointmentForm,\
    HiddenForm, RegionChooseForm, DatePickForm


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


def get_free_count(date, timeslot, region):
    """ Given a date, timeslot and region return the number of free slots """
    query = Calendar.objects.filter(date=date)
    query = query.filter(timeslot=timeslot)
    query = query.filter(region=region)
    calendar_entries = query.all()
    if not calendar_entries:
        return 4
    else:
        entry = calendar_entries[0]
        left = 4 - len(entry.appointment_set.all())
        return left


def get_free_entries(fromDate, daysAhead, region):
    """ Return a list of quadrupels containing date, timeslot,
     regions and number of free slots.
     A quadrupel with no free slots is left out. """
    result = []
    for offset in range(0, daysAhead):
        date = fromDate + datetime.timedelta(days=offset)
        timeslots = get_timeslots(date, region)
        for ts in timeslots:
            free_count = get_free_count(date, ts, region)
            if free_count > 0:
                result.append((date, ts, region, free_count))
    return result


def get_timeslots(date, region):
    """ Returns a list of timeslots for the given region on the given date. """
    timeslots = region.timeslots.all()
    week_day = date.weekday() + 1
    return get_timeslots_for_day_of_week(week_day, timeslots)


def get_timeslots_for_day_of_week(dayOfWeek, timeslots):
    """ Filters a list of timeslots down to a weekday """
    return filter(lambda x: x.day_of_week == dayOfWeek, timeslots)


def get_date_from_iso(iso_date):
    """ Returns a date object corresponding to the given iso-date string. """
    return datetime.datetime.strptime(iso_date, '%Y%m%d').date()


def get_or_create_calendar(timeslot_id, region_id, date):
    """ Return exiting calendar object for this triplet or creates one 
    if non-existent"""
    calendars = Calendar.objects.filter(date=date).filter(timeslot__pk=timeslot_id).filter(region__pk=region_id)
    if calendars:
        calendar = calendars[0]
    else:
        calendar = Calendar()
        calendar.date = date
        calendar.timeslot = TimeSlot.objects.get(pk=int(timeslot_id))
        calendar.region = Region.objects.get(pk=int(region_id))
        calendar.save()
    return calendar


@group_required('Callcenter')
def create_appointment(request):
    """ Saves an Appointment, Customer and Calendar object corresponding to a
    real world appointment. """
    if not request.POST:
        raise Exception()
    appointment = Appointment()
    customerForm = CustomerForm(request.POST)
    if customerForm.is_valid():  # Customer form valid, save Cutomer
        customer = customerForm.save()
        appointment.customer = customer
        appointment.employee = request.user
        appointmentForm = AppointmentForm(request.POST, instance=appointment)
        if appointmentForm.is_valid():  # Both valid, so save
            hiddenForm = HiddenForm(request.POST)
            calendar = None
            if hiddenForm.is_valid():
                timeslot_id = hiddenForm.cleaned_data['timeslot_id']
                region_id = hiddenForm.cleaned_data['region_id']
                date = hiddenForm.cleaned_data['date']
                               
                appointment.calendar = get_or_create_calendar(timeslot_id, region_id, date)
                app = appointmentForm.save()
                return redirect('AppointmentView',  app.id)
        else:  # Appointment not valid, so rerender with errors
            customer.delete()
    else:  # Customer not valid rerender with errors
        appointmentForm = AppointmentForm(request.POST)
        appointmentForm.is_valid()
    hiddenForm = HiddenForm(request.POST)
    return render_to_response('appointment.html',
         {"appointmentForm": appointmentForm,
         "title": "Appointment details",
         "customerForm": customerForm,
         "hiddenForm": hiddenForm, },
         context_instance=RequestContext(request))

def tomorrow():
    return (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y%m%d')

@group_required('Callcenter')
def chose_a_region(request, date_iso):
    if not date_iso:
        date_iso=tomorrow()
    if not request.POST:
        form = RegionChooseForm()
        return render_to_response('region.html',
                                  {"form": form, "title": "Choose a region" },
                                   context_instance=RequestContext(request))
    else:
        form = RegionChooseForm(request.POST)
        if form.is_valid():
            region = form.cleaned_data['region']
            free_space = get_free_entries(get_date_from_iso(date_iso),
                                           14, region)
            free_space_readable = []
            for space in free_space:
                free_space_readable.append(space[0].strftime('%d %B ')  + str(space[1]))
        return render_to_response('choose_a_date.html',
                                   { "title": "Choose a date",
                                     "free_space": free_space_readable,
                                     "region_id": region.id,
                                     "date_iso": date_iso },
                                  context_instance=RequestContext(request))

@group_required('Callcenter')
def chosen_date(request, date_iso):
    if not date_iso:
        date_iso=tomorrow()
    region = Region.objects.get(pk=request.POST['region_id'])
    free_space = get_free_entries(get_date_from_iso(date_iso), 14, region)
    index = int(request.POST['free_space']) - 1
    free = free_space[index]
    timeslot_id = free[1].id
    date = free[0]
    appointmentForm = AppointmentForm()
    customerForm = CustomerForm()
    hiddenForm = HiddenForm({'timeslot_id':timeslot_id, 'date': date, 'region_id':region.id})
    return render_to_response('appointment.html',
                              {"appointmentForm": appointmentForm,
                               "title": "Appointment details",
                               "customerForm": customerForm,
                               "hiddenForm": hiddenForm,
                                },
                               context_instance=RequestContext(request))

@group_required('Callcenter')
def display_date_form(request):
    form = DatePickForm({"date": datetime.date.today() + datetime.timedelta(days=1) })
    return render_to_response('choose_appointment_list.html',
                               {'title':'Pick a date',
                                'form': form },
                                context_instance=RequestContext(request))


@group_required('Callcenter')
def list_date_chosen(request):
    form = DatePickForm(request.POST)
    if form.is_valid():
        date = form.cleaned_data['date']
        cals = Calendar.objects.filter(date=date)
    else:
        cals =[]
    return render_to_response('choose_calendar.html',
                              {"title": "Choose a region and timeslot",
                               'calendar_list':cals},
                              context_instance=RequestContext(request))

@group_required('Callcenter')
def render_appointment_list(request):
    calendar_id = request.GET['calendar_id']
    calendar = Calendar.objects.get(pk=calendar_id)
    return render_to_response('appointment_list.html',
                               {"title": "Appointment list",
                                'region': calendar.region,
                                'date': calendar.date.strftime('%A %d %B %Y'),
                                'timeslot': calendar.timeslot,
                                'app_list': calendar.appointment_set.all()
                                })

@group_required('Callcenter')
def calendar_search_view(request):
    search_results = []
    if not request.POST:
        search_form = CalendarSearchForm()
    else:
        search_form = CalendarSearchForm(request.POST)
        if search_form.is_valid():
            search_results = Appointment.objects.filter(customer__name__icontains=search_form.cleaned_data['name'])
    logging.error("No of search results %d" % len(search_results) )
    return render_to_response('calendar_search_view.html',
                              {"search_form": search_form,
                               "search_results": search_results,
                               "title": "Customer search"},
                              context_instance=RequestContext(request))




