# Create your views here.
from __future__ import absolute_import
from .__init__ import group_required, get_date_from_iso, tomorrow
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from .models import Appointment, Calendar, Customer
from .forms import CustomerForm, AppointmentForm, HiddenForm
from .schedule import get_free_entries, get_free_entries_with_extra_calendar
from django.contrib.auth.views import logout
import logging
from django.utils import simplejson
from django.http import HttpResponse
from planner.area.views import get_regions_for_postcalcode
from planner.main.schedule import get_total_weight
from django.forms.util import ErrorList
from planner.main.schedule import APPOINTMENTS_PER_HALF_DAY

STANDARD_DAYS_AHEAD = 28

def space_available(calendar_id_string, appointment_form, appointment_id):
    """ Assumes appointment_form's  is_valid was called and returned True"""
    if calendar_id_string:
        calendar_id = int(calendar_id_string)
        calendar = Calendar.objects.get(pk=calendar_id)
        existing_apps = calendar.active_appointments()
        kind = appointment_form.cleaned_data['kind']
        old_weight = 0
        if not appointment_id == 'create':
            app = Appointment.actives.get(pk=int(appointment_id))
            old_weight = app.weight
        
        weight = get_total_weight(existing_apps, kind) - old_weight
        
        aw = int(appointment_form.cleaned_data['weight'])
        return weight + aw <= APPOINTMENTS_PER_HALF_DAY
    else:
        return False


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
        else:  # customer_id is set
            title = _("Follow up appointment")
            appointment.customer = Customer.objects.get(pk=int(customer_id))
    else:  # appointment_id is set
        title = _("Edit or move appointment")
        appointment = Appointment.objects.get(pk=int(appointment_id))
        calendar_id = appointment.calendar.pk
    if request.method == 'GET':
        hidden_form = HiddenForm()
        appointment_form = AppointmentForm(instance=appointment)
        customer_form = CustomerForm(instance=appointment.customer)
    else:  # POST
        hidden_form = HiddenForm(request.POST)
        if hidden_form.is_valid():
            customer_id = hidden_form.cleaned_data['found_customer_id']
            if customer_id:
                logging.error("Customer known")
                appointment.customer = Customer.objects.get(pk=customer_id)
        else:
            logging.error("Customer unknown")
        appointment_form = AppointmentForm(request.POST,
                                              instance=appointment)
        customer_form = CustomerForm(request.POST,
                                     instance=appointment.customer)
        free_space = request.POST.get('free_space', '')
        app_valid = appointment_form.is_valid()
        if app_valid:
            if space_available(free_space, appointment_form, appointment_id):
                if customer_form.is_valid():
                    calendar_id = int(free_space)
                    appointment.calendar = Calendar.objects.get(pk=calendar_id)
                    appointment.employee = request.user
                    logging.error(appointment.calendar)
                    customer = customer_form.save()
                    appointment.customer = customer
                    appointment = appointment_form.save()
                    return redirect('AppointmentView', appointment.id)
            else:
                appointment_form._errors['weight'] = \
                    ErrorList([_("No more space left")])

    return render_to_response('appointment_manipulation.html',
                              {"appointmentForm": appointment_form,
                               "title": title,
                               "customerForm": customer_form,
                               "hiddenForm": hidden_form,
                               "date_iso": date_iso,
                               "calendar_id": calendar_id,
                               },
                              context_instance=RequestContext(request))

def get_region_description(regions):
    if regions:
        return str(map (lambda x: str(x.name), regions))
    else:
        return _("Unknown")

@group_required('Callcenter')
def get_candidate_dates(
                        request,
                        date_iso,
                        weight,
                        postalcode,
                        car_id,
                        kind,
                        calendar_id                   
                        ):
    date = get_date_from_iso(date_iso)
    weight = int(weight)
    
    if not postalcode == "-1":
        # normal pick-up case
        regions = get_regions_for_postcalcode(postalcode)
        region_code = get_region_description(regions)
    else:
        if car_id == "-1":
            regions = None
            region_code = _("Unrestricted")
        else:
            pass
        
        
    if calendar_id == "-1":
        #new case
        available_dates = get_free_entries(date,
                                           STANDARD_DAYS_AHEAD,
                                           regions,
                                           weight,
                                           kind,
                                           car_id) 
    else:
        #edit case
        calendar = Calendar.objects.get(pk=int(calendar_id))
        available_dates = get_free_entries_with_extra_calendar(date,
                                           STANDARD_DAYS_AHEAD,
                                           regions,
                                           weight,
                                           kind,
                                           car_id,
                                           calendar)
        
    data = {'region': region_code, 'dates': available_dates}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')
        
        
        
        
@group_required('Callcenter')
def get_available_dates(request,
                        postalcode,
                        weight,
                        date_iso,
                        calendar_id,
                        unrestricted=False,
                        car_id=-1):
    """ Returns a json object to fill the calendar choices component """
    logging.error("%s %s" % (postalcode, weight))
    if unrestricted:
        regions = None
        region_code = _("Unrestricted")
    else:
        regions = get_regions_for_postcalcode(postalcode)
        region_code = get_region_description(regions)
    if calendar_id == "-1":
        available_dates = get_free_entries(get_date_from_iso(date_iso),
                                           STANDARD_DAYS_AHEAD, regions, int(weight), 2, None)
    else:
        calendar = Calendar.objects.get(pk=int(calendar_id))
        date = get_date_from_iso(date_iso)
        available_dates = get_free_entries_with_extra_calendar(date,
                                                               STANDARD_DAYS_AHEAD,
                                                               regions,
                                                               int(weight), 2, None,
                                                               calendar)
    data = {'region': region_code, 'dates': available_dates}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')


@group_required('Callcenter')
def get_customer(request, postalcode, number, addition):
    """ Returns a json object to fill the calendar choices component """
    logging.error("%s %s %s" % (postalcode, number, addition))
    customer = Customer.objects.get(postcode=postalcode.capitalize(),
                                    number=number, additions=addition)
    data = {'name': customer.name,
            'address': customer.address,
            'town': customer.town,
            'phone': customer.phone,
            'id': customer.id,
            'email': customer.email}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype='application/json')


def logout_view(request):
    logout(request)
    return redirect('Overview', '')


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
        return redirect('Overview', '')
