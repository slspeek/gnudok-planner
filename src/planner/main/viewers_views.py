""" Read-only views """
from __future__ import absolute_import
from .__init__ import tomorrow, get_date_from_iso, group_required, to_iso
import logging
import datetime
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from .models import Appointment, Calendar, Car
from .forms import CalendarSearchForm, DatePickForm
from .schedule import get_region, get_total_weight

@group_required('Viewers')
def overview(request):
    car_list = Car.objects.all()
    return render_to_response("main/overview.html", 
                              {"title": _("Overview"),
                               "car_list": car_list,
                               "range": [("-1", _("Last week")),
                                          ("0", _("This week")),
                                          ("1", _("Next week"))]})
    
    
@group_required('Viewers')
def weekview(request, car_id=0 , offset=0, date_iso=""):
    if not date_iso:
        date_iso=tomorrow()
    begin_date = get_date_from_iso(date_iso) + datetime.timedelta(weeks=int(offset))
    end_date = begin_date + datetime.timedelta(weeks=1)
    queryset = Calendar.objects.filter(car__pk=int(car_id))
    calendars = queryset.filter(date__range=[begin_date, end_date]).all()
    for cal in calendars:
        app_list = filter(lambda x:x.status == 1, cal.appointment_set.all())
        free_count = 4 - get_total_weight(app_list)
        cal.free = free_count
        cal.region = get_region(cal)
        
    car = Car.objects.get(pk=int(car_id))
    return render_to_response("calendar_week.html",
                               {"object_list": calendars,
                                "from": begin_date,
                                "to": end_date,
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
                                'Car': calendar.car,
                                'date': calendar.date,
                                'timeslot': calendar.timeslot,
                                'app_list': filter(lambda x:x.status == 1,calendar.appointment_set.all())
                                })

@group_required('Viewers')
def calendar_search_view(request):
    search_results = []
    if not request.POST:
        search_form = CalendarSearchForm()
    else:
        search_form = CalendarSearchForm(request.POST)
        if search_form.is_valid():
            search_results = Appointment.objects.filter(customer__name__icontains=search_form.cleaned_data['name'], status=1)
    logging.error("No of search results %d" % len(search_results) )
    return render_to_response('calendar_search_view.html',
                              {"search_form": search_form,
                               "search_results": search_results,
                               "title": _("Customer search")},
                              context_instance=RequestContext(request))




