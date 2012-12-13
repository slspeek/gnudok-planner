# Create your views here.
from __future__ import absolute_import
from .__init__ import group_required, get_date_from_iso, tomorrow
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from .models import Appointment, Calendar, Region, Customer
from .forms import  CustomerForm, AppointmentForm, \
    RegionChooseForm, BigAppointmentForm, HiddenForm
from .schedule import get_free_entries, get_region, get_free_entries_with_extra_calendar
from django.contrib.auth.views import logout
import logging
from django.utils import simplejson
from django.http import HttpResponse
from planner.area.views import get_region_for_postcalcode

@group_required('Callcenter')
def appointment_manipulation(request, appointment_id, customer_id, date_iso):
    """ creates or edits an appointment and customer """
    if not date_iso:
        date_iso = tomorrow()
    if appointment_id == 'create':
        appointment = Appointment()
        calendar_id = "-1"
        if customer_id == 'create':
            title = _("New appointment")
            appointment.customer = Customer()
        else: # customer_id is set
            title = _("Follow up appointment")
            appointment.customer = Customer.objects.get(pk=int(customer_id))
    else: # appointment_id is set
        title = _("Edit or move appointment")
        appointment = Appointment.objects.get(pk=int(appointment_id))
        calendar_id = appointment.calendar.pk
    if request.method == 'GET':
        hidden_form = HiddenForm()
        appointment_form = BigAppointmentForm(instance=appointment)
        customer_form = CustomerForm(instance=appointment.customer)
    else: # POST
        hidden_form = HiddenForm(request.POST)
        if hidden_form.is_valid():
            customer_id = hidden_form.cleaned_data['found_customer_id']
            appointment.customer = Customer.objects.get(pk=customer_id)
        appointment_form = BigAppointmentForm(request.POST,instance=appointment)
        customer_form = CustomerForm(request.POST,instance=appointment.customer)
        free_space = request.POST.get('free_space', '') 
        if appointment_form.is_valid() and customer_form.is_valid() and free_space:
            calendar_id = int(free_space)
            appointment.calendar = Calendar.objects.get(pk=calendar_id)
            customer = customer_form.save()
            appointment = appointment_form.save()
            #appointment.save()
            return redirect('AppointmentView', appointment.id)
            
    return render_to_response('appointment_manipulation.html',
     {"appointmentForm": appointment_form,
     "title": title,
     "customerForm": customer_form,
     "hiddenForm": hidden_form,
     "date_iso": date_iso,
     "calendar_id": calendar_id,
      },
     context_instance=RequestContext(request))

@group_required('Callcenter') 
def get_available_dates(request, postalcode, weight, date_iso):
    """ Returns a json object to fill the calendar choices component """
    logging.error("%s %s" % (postalcode, weight))
    region = get_region_for_postcalcode(postalcode)
    available_dates = get_free_entries(get_date_from_iso(date_iso),
                                       28, region, int(weight))
    dates = []
    for a_date in available_dates:
        dates.append((a_date[0], a_date[1]))
    data = {'region':region.name, 'dates': dates }
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')

@group_required('Callcenter') 
def get_customer(request, postalcode, number, addition):
    """ Returns a json object to fill the calendar choices component """
    logging.error("%s %s %s" % (postalcode, number, addition))
    customer = Customer.objects.get(postcode=postalcode.capitalize(), number=number, additions=addition)
    data = {'name':customer.name,
            'address':customer.address,
            'town': customer.town,
            'phone': customer.phone,
            'id': customer.id,
            'email': customer.email }
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')

    
def logout_view(request):
    logout(request)
    return redirect('Overview')

@group_required('Callcenter')
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(pk=int(appointment_id))
    if not request.method == 'POST':
        return render_to_response('appointment_cancel.html',
                                  {'object': appointment},
                                  context_instance=RequestContext(request)
                                  )
    else:
        appointment.status = 2
        appointment.save()
        return redirect('Overview')
        

@group_required('Callcenter')
def edit_appointment(request, appointment_id=0, date_iso=""):
    if not date_iso:
        date_iso = tomorrow()
    if appointment_id == 'create':
        appointment = Appointment() 
        free_space = []
    else:
        appointment = Appointment.objects.get(pk=int(appointment_id))
        region = get_region(appointment.calendar)
        free_space = get_free_entries_with_extra_calendar(get_date_from_iso(date_iso), 28, region, appointment.weight, appointment.calendar)
        
    if request.method == 'GET' and not appointment_id == 'create':
        appointmentForm = AppointmentForm(instance=appointment)
        customerForm = CustomerForm(instance=appointment.customer)
    elif request.method == 'GET' and appointment_id == 'create':
        appointmentForm = AppointmentForm()
        customerForm = CustomerForm()
        
    else:
        appointmentForm = AppointmentForm(request.POST, instance=appointment)
        calendar_id = int(request.POST['free_space'])
        customerForm = CustomerForm(request.POST, instance=appointment.customer)
        if appointmentForm.is_valid() and customerForm.is_valid():
            appointment = appointmentForm.save(commit=False)
            appointment.calendar = Calendar.objects.get(pk=calendar_id)
            appointment.save()
            customerForm.save()
            return redirect('AppointmentView', appointment.id)
    return render_to_response('edit_appointment.html',
     {"appointmentForm": appointmentForm,
     "title": _("Edit or Move appointment"),
     "customerForm": customerForm,
     "free_space": free_space,
     "calendar_id": appointment.calendar.pk,
      },
     context_instance=RequestContext(request))
        

@group_required('Callcenter')
def create_appointment(request, calendar_id, weight):
    """ Saves an Appointment and Customer object corresponding to a
    real world appointment. """
    if request.POST:
        appointment = Appointment()
        customerForm = CustomerForm(request.POST)
        if customerForm.is_valid():  # Customer form valid, save Cutomer
            customer = customerForm.save()
            appointment.customer = customer
            appointment.employee = request.user
            appointmentForm = AppointmentForm(request.POST, instance=appointment)
            if appointmentForm.is_valid():  # Both valid, so save
                appointment.weight = int(weight)
                appointment.calendar = Calendar.objects.get(pk=int(calendar_id))
                app = appointmentForm.save()
                return redirect('AppointmentView', app.id)
            else:  # Appointment not valid, so rerender with errors
                customer.delete()
        else:  # Customer not valid rerender with errors
            appointmentForm = AppointmentForm(request.POST)
            appointmentForm.is_valid()
    else:
        appointmentForm = AppointmentForm()
        customerForm = CustomerForm()
    return render_to_response('appointment.html',
         {"appointmentForm": appointmentForm,
         "title": _("Appointment details"),
         "customerForm": customerForm
          },
         context_instance=RequestContext(request))


@group_required('Callcenter')
def chose_a_region(request, date_iso):
    if not date_iso:
        date_iso = tomorrow()
    
    if request.POST:
        region_form = RegionChooseForm(request.POST)
        if region_form.is_valid():
            region = region_form.cleaned_data['region']
            weight = int(region_form.cleaned_data['weight'])
            return redirect(choose_a_date, region.pk, weight, date_iso)
    else:
        region_form = RegionChooseForm()
    return render_to_response('region.html',
                              {"form": region_form, "title": _("Choose a region") },
                               context_instance=RequestContext(request))

@group_required('Callcenter')
def choose_a_date(request, region_id, weight, date_iso):
    if not date_iso:
        date_iso = tomorrow()
    region = Region.objects.get(pk=region_id)
    free_space = get_free_entries(get_date_from_iso(date_iso),
                                       28, region, int(weight))
    if request.POST:
        chosen_calendar = request.POST['free_space']
        return redirect(create_appointment, chosen_calendar, weight)
    return render_to_response('choose_a_date.html',
                                   { "title": _("Choose a date"),
                                     "free_space": free_space,
                                      },
                                  context_instance=RequestContext(request))    
