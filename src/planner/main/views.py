# Create your views here.
from __future__ import absolute_import
import logging
import datetime
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import user_passes_test
from .models import Appointment, Calendar
from .forms import CalendarSearchForm, CustomerForm, AppointmentForm,\
    HiddenForm, RegionChooseForm, DatePickForm
from .schedule import get_free_entries, get_region


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@group_required('Callcenter')
def edit_appointment(request, appointment_id=0, date_iso=""):
    if not date_iso:
        date_iso=tomorrow()

    appointment = Appointment.objects.get(pk=int(appointment_id))
    if not request.POST:
        appointmentForm = AppointmentForm(instance=appointment)
        customerForm = CustomerForm(instance=appointment.customer)
        region = get_region(appointment.calendar)
        free_space = get_free_entries(get_date_from_iso(date_iso), 14, region, appointment.weight)
        return render_to_response('edit_appointment.html',
             {"appointmentForm": appointmentForm,
             "title": "Edit or Move appointment",
             "customerForm": customerForm,
             "free_space": free_space,
             "calendar_id": appointment.calendar.pk,
              },
             context_instance=RequestContext(request))
    else:
        appointmentForm = AppointmentForm(request.POST, instance=appointment)
        calendar_id = int(request.POST['free_space'])
        customerForm = CustomerForm(request.POST, instance=appointment.customer)
        if appointmentForm.is_valid() and customerForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.calendar = Calendar.objects.get(pk=calendar_id)
            appointment.save()
            customerForm.save()
            return redirect('AppointmentView',  appointment.id)
        else:
            return render_to_response('edit_appointment.html',
             {"appointmentForm": appointmentForm,
             "title": "Edit or Move appointment",
             "customerForm": customerForm,
             "free_space": free_space,
             "calendar_id": appointment.calendar.pk,
              },
             context_instance=RequestContext(request))
            

        

@group_required('Callcenter')
def create_appointment(request):
    """ Saves an Appointment and Customer object corresponding to a
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
                calendar_id = hiddenForm.cleaned_data['calendar_id']
                weight = hiddenForm.cleaned_data['weight']
                appointment.weight = weight
                appointment.calendar = Calendar.objects.get(pk=int(calendar_id))
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
        region_form = RegionChooseForm(request.POST)
        if region_form.is_valid():
            region = region_form.cleaned_data['region']
            weight = int(region_form.cleaned_data['weight'])
            free_space = get_free_entries(get_date_from_iso(date_iso),
                                           14, region, weight)
        return render_to_response('choose_a_date.html',
                                   { "title": "Choose a date",
                                     "free_space": free_space,
                                     "region_id": region.id,
                                     "weight": weight,
                                     "date_iso": date_iso },
                                  context_instance=RequestContext(request))

@group_required('Callcenter')
def chosen_date(request, date_iso):
    if not date_iso:
        date_iso=tomorrow()
    
    weight = int(request.POST['weight'])
    free_space = request.POST['free_space']
    
    appointmentForm = AppointmentForm()
    customerForm = CustomerForm()
    hiddenForm = HiddenForm({'weight': weight, 'calendar_id':free_space})
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




