""" Read-only views """
from __future__ import absolute_import
from .__init__ import tomorrow, get_date_from_iso, group_required, to_iso
from django.contrib.auth.models import User
import logging
import datetime
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from .models import Appointment, Calendar, Car
from .forms import CalendarSearchForm, DatePickForm
from .schedule import get_region, get_total_weight


@group_required('Viewers')
def appointment_detail(request, pk):
    appointment = Appointment.objects.get(pk=int(pk))
    region = get_region(appointment.calendar)
    return render_to_response("main/appointment_detail.html", 
                              {
                               "object": appointment,
                               "region": region,
                               })


@group_required('Viewers')
def appointments_made_today(request, date_iso):
    if not date_iso:
        date_iso=datetime.date.today().strftime('%Y%m%d')
    date = get_date_from_iso(date_iso)
    appointment_list = Appointment.actives.filter(created__range=[date, date + datetime.timedelta(days=1 )])
    return render_to_response("appointments_today.html", 
                              {"date": date,
                               "appointment_list": appointment_list,
                               })

@group_required('Viewers')
def appointments_made_by(request, employee_id):
    appointment_list = Appointment.actives.filter(employee__pk=employee_id)
    return render_to_response("appointments_made_by.html", 
                              {"employee": User.objects.get(pk=employee_id),
                               "appointment_list": appointment_list,
                               })

@group_required('Viewers')
def overview(request, date_iso):
    if not date_iso:
        date_iso=tomorrow()
    range_list = []
    for counter in range(-2, 4):
        begin, end = get_date_interval(date_iso, counter)
        range_list.append((counter, begin, end))
    car_list = Car.objects.all()
    return render_to_response("main/overview.html", 
                              {"title": _("Overview"),
                               "date_iso": date_iso,
                               "car_list": car_list,
                               "range": range_list,
                               })
    
def get_date_interval(date_iso, offset):
    begin_date = get_date_from_iso(date_iso) + datetime.timedelta(weeks=int(offset))
    end_date = begin_date + datetime.timedelta(weeks=1)
    return (begin_date, end_date)

@group_required('Viewers')
def weekview(request, car_id=0 , offset=0, date_iso=""):
    if not date_iso:
        date_iso=tomorrow()
    offset = int(offset)
    begin_date, end_date = get_date_interval(date_iso, offset)
    queryset = Calendar.objects.filter(car__pk=int(car_id))
    calendars = queryset.filter(date__range=[begin_date, end_date]).all()
    for cal in calendars:
        app_list = cal.active_appoinments().all()
        free_count = 4 - get_total_weight(app_list)
        cal.free = free_count
        cal.region = get_region(cal)
        
    car = Car.objects.get(pk=int(car_id))
    return render_to_response("calendar_week.html",
                               {"object_list": calendars,
                                "from": begin_date,
                                "to": end_date,
                                "next": offset + 1,
                                "prev": offset - 1,
                                "car":car})


@group_required('Viewers')
def display_date_form(request):
    if not request.POST:
        form = DatePickForm({"date": datetime.date.today() + datetime.timedelta(days=1) })
    else:
        form = DatePickForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            return redirect(choose_calendar, to_iso(date))
    return render_to_response('choose_listing_date.html',
                               {'title': _('Pick a date'),
                                'form': form },
                                context_instance=RequestContext(request))


@group_required('Viewers')
def choose_calendar(request, date_string):
    date = get_date_from_iso(date_string)
    cals = Calendar.objects.filter(date=date)
    return render_to_response('choose_calendar.html',
                              {"title": _("Choose a region and timeslot"),
                               'calendar_list':cals},
                              context_instance=RequestContext(request))

@group_required('Viewers')
def render_appointment_list(request, calendar_id):
    calendar = Calendar.objects.get(pk=int(calendar_id))
    return render_to_response('appointment_list.html',
                               {"title": _("Appointment list"),
                                'car': calendar.car,
                                'date': calendar.date,
                                'region': get_region(calendar),
                                'timeslot': calendar.timeslot,
                                'app_list': calendar.active_appoinments().all()
                                })

@group_required('Viewers')
def calendar_search_view(request):
    search_results = []
    result_count = 0
    if not request.POST:
        search_form = CalendarSearchForm()
        searched = False
    else:
        search_form = CalendarSearchForm(request.POST)
        if search_form.is_valid():
            search_results = Appointment.actives.filter(customer__name__icontains=search_form.cleaned_data['name'])
            searched = True
            result_count = len(search_results)
    return render_to_response('calendar_search_view.html',
                              {"search_form": search_form,
                               "searched": searched,
                               "result_count": result_count,
                               "search_results": search_results,
                               "title": _("Customer search")},
                              context_instance=RequestContext(request))




