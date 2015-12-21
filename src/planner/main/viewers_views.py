""" Read-only views """
from __future__ import absolute_import
import datetime
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required
from planner.main.models import Appointment, Calendar, Car, Customer, KIND_PICKUP
from planner.main import today, tomorrow, get_date_from_iso, to_iso
from planner.main.forms import CalendarSearchForm, DatePickForm, EmployeeChooseForm
from planner.main.schedule import get_region_name, get_total_weight, get_limit

@permission_required('main.viewers')
def wrong_postcode(_):
    all_customers = Customer.objects.order_by('postcode').all()
    customers = [x for  x in all_customers if not x.postcode.isupper()]
    return render_to_response("main/wrong_postcode.html",
                              {"customers": customers,
                              })

@permission_required('main.viewers')
def appointment_detail(_, pk):
    # pylint: disable=E1101
    appointment = Appointment.objects.get(pk=int(pk))
    region_name = get_region_name(appointment.calendar)
    return render_to_response("main/appointment_detail.html",
                              {"object": appointment,
                               "region_name": region_name, })


@permission_required('main.viewers')
def choose_an_employee(request):
    if request.POST:
        form = EmployeeChooseForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            return redirect(appointments_made_by, employee.pk)
    else:
        form = EmployeeChooseForm()
    return render_to_response('choose_an_employee.html',
                              {"form": form,
                               "title": _("Choose an employee")},
                              context_instance=RequestContext(request))


@permission_required('main.viewers')
def appointments_by_date(_, date_iso):
    # pylint: disable=E1101
    if not date_iso:
        date_iso = datetime.date.today().strftime('%Y%m%d')
    date = get_date_from_iso(date_iso)
    date_interval = [date, date + datetime.timedelta(days=1)]
    unordered = Appointment.actives.filter(created__range=date_interval)
    appointment_list = unordered.order_by('-created')
    return render_to_response("appointments_today.html",
                              {"date": date,
                               "appointment_list": appointment_list,
                              })


@permission_required('main.viewers')
def appointments_made_by(_, employee_id):
    # pylint: disable=E1101
    by_one_employee = Appointment.actives.filter(employee__pk=employee_id)
    appointment_list = by_one_employee.order_by('calendar__date')

    employee = User.objects.get(pk=employee_id)
    return render_to_response("appointments_made_by.html",
                              {"employee": employee,
                               "appointment_list": appointment_list,
                              })


@permission_required('main.viewers')
def overview(request, date_iso):
    # pylint: disable=w0613
    if not date_iso:
        date_iso = tomorrow()
    range_list0, range_list1, range_list2 = [], [], []
    for counter in range(-2, 0):
        begin, end = get_date_interval(date_iso, counter)
        range_list0.append((counter, begin, end))
    for counter in range(0, 1):
        begin, end = get_date_interval(date_iso, counter)
        range_list1.append((counter, begin, end))
    for counter in range(1, 4):
        begin, end = get_date_interval(date_iso, counter)
        range_list2.append((counter, begin, end))
    car_list = Car.objects.all()
    return render_to_response("main/overview.html",
                              {"title": _("Overview"),
                               "date_iso": date_iso,
                               "car_list": car_list,
                               "range0": range_list0,
                               "range1": range_list1,
                               "range2": range_list2,
                              })


def get_date_interval(date_iso, offset):
    begin_date = get_date_from_iso(date_iso) + \
        datetime.timedelta(weeks=int(offset))
    end_date = begin_date + datetime.timedelta(weeks=1)
    return (begin_date, end_date)


@permission_required('main.viewers')
def weekview(_, car_id=0, offset=0, date_iso=""):
    if not date_iso:
        date_iso = tomorrow()
    offset = int(offset)
    begin_date, end_date = get_date_interval(date_iso, offset)
    queryset = Calendar.objects.filter(car__pk=int(car_id))
    calendars = queryset.filter(date__range=[begin_date, end_date]).all()
    for cal in calendars:
        app_list = cal.active_appointments().all()
        free_count = get_limit(KIND_PICKUP) - get_total_weight(app_list, KIND_PICKUP)
        cal.free = free_count
        cal.region_name = get_region_name(cal)
        cal.appointments = cal.active_appointments().all()

    car = Car.objects.get(pk=int(car_id))
    return render_to_response("calendar_week.html",
                              {"object_list": calendars,
                               "from": begin_date,
                               "to": end_date,
                               "next": offset + 1,
                               "prev": offset - 1,
                               "car": car})


@permission_required('main.viewers')
def display_date_form(request):
    if not request.POST:
        tommorrow = datetime.date.today() + datetime.timedelta(days=1)
        form = DatePickForm({"date": tommorrow})
    else:
        form = DatePickForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            return redirect(choose_calendar, to_iso(date))
    return render_to_response('choose_listing_date.html',
                              {'title': _('Pick a date'),
                               'form': form},
                              context_instance=RequestContext(request))


@permission_required('main.viewers')
def choose_calendar(request, date_string):
    date = get_date_from_iso(date_string)
    cals = Calendar.objects.filter(date=date)
    return render_to_response('choose_calendar.html',
                              {"title": _("Choose a region and timeslot"),
                               'calendar_list': cals},
                              context_instance=RequestContext(request))


@permission_required('main.viewers')
def render_appointment_list(_, calendar_id):
    calendar = Calendar.objects.get(pk=int(calendar_id))
    title = calendar.date.strftime('%d %b') + ':' + str(calendar.car) + str(calendar.timeslot.begin)

    return render_to_response('appointment_list.html',
                              {"title": title,
                               'car': calendar.car,
                               'date': calendar.date,
                               'region_name': get_region_name(calendar),
                               'timeslot': calendar.timeslot,
                               'app_list': calendar.active_appointments().all()
                              })

def normalize_postalcode(postalcode):
    result = postalcode.replace(' ', '')
    return result.strip()

def search(search_form, date_iso=''):
    # pylint: disable=E1101,R0916,R0204
    if not date_iso:
        date_iso = today()
    include_past = search_form.cleaned_data['include_past']
    include_cancelled = search_form.cleaned_data['include_cancelled']
    if include_cancelled:
        results = Appointment.objects
    else:
        results = Appointment.actives
    if not include_past:
        date = get_date_from_iso(date_iso)
        results = results.filter(calendar__date__gte=date)
    name = search_form.cleaned_data['name']
    if name:
        results = results.filter(customer__name__icontains=name)
    postcode = search_form.cleaned_data['postcode']
    if postcode:
        postcode = normalize_postalcode(postcode)
        results = results.filter(customer__postcode__icontains=postcode)
    street = search_form.cleaned_data['street']
    if street:
        results = results.filter(customer__address__icontains=street)
    town = search_form.cleaned_data['town']
    if town:
        results = results.filter(customer__town__icontains=town)
    date = search_form.cleaned_data['date']
    if date:
        results = results.filter(calendar__date=date)
    stuff = search_form.cleaned_data['stuff']
    if stuff:
        results = results.filter(stuff__icontains=stuff)
    phone = search_form.cleaned_data['phone']
    if phone:
        results = results.filter(customer__phone__icontains=phone)
    # Is this needed?
    if not name and (not postcode) and not date and not street and not stuff and not phone:
        results = results.all()
    return results


@permission_required('main.viewers')
def calendar_search_view(request, date_iso=""):
    # pylint: disable=R0204
    if not date_iso:
        date_iso = today()
    results = []
    result_count = 0
    if not request.POST:
        search_form = CalendarSearchForm()
        searched = False
    else:
        search_form = CalendarSearchForm(request.POST)
        if search_form.is_valid():
            results = search(search_form, date_iso)
            result_count = len(results)
            searched = True
    return render_to_response('calendar_search_view.html',
                              {"search_form": search_form,
                               "searched": searched,
                               "result_count": result_count,
                               "search_results": results,
                               "title": _("Customer search")},
                              context_instance=RequestContext(request))
