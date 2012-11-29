# Create your views here.
from __future__ import absolute_import
import logging
import datetime
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import user_passes_test
from .models import Appointment, Region, Calendar
from .forms import CalendarSearchForm, CustomerForm, AppointmentForm,\
    HiddenForm, RegionChooseForm, DatePickForm
from .schedule import get_free_entries, get_or_create_calendar


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)



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
            if hiddenForm.is_valid():
                timeslot_id = hiddenForm.cleaned_data['timeslot_id']
                car_id = hiddenForm.cleaned_data['car_id']
                date = hiddenForm.cleaned_data['date']
                               
                appointment.calendar = get_or_create_calendar(timeslot_id, car_id, date)
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


def get_date_from_iso(iso_date):
    """ Returns a date object corresponding to the given iso-date string. """
    return datetime.datetime.strptime(iso_date, '%Y%m%d').date()


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
    chosen_rule = free_space[index]
    timeslot_id = chosen_rule[1].timeslot.pk
    car_id = chosen_rule[1].car.pk
    date = chosen_rule[0]
    appointmentForm = AppointmentForm()
    customerForm = CustomerForm()
    hiddenForm = HiddenForm({'timeslot_id':timeslot_id, 'date': date, 'car_id':car_id})
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
                                'Car': calendar.car,
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




