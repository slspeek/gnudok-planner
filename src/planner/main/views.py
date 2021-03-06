# Create your views here.
from __future__ import absolute_import
import json
import logging
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
from django.http import HttpResponse
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import permission_required
from planner.main.schedule import get_free_entries, get_free_entries_with_extra_calendar
from planner.main.models import Appointment, Calendar, Customer, Car
from planner.main.forms import CustomerForm, AppointmentForm, HiddenForm, CarForm
from planner.main import get_date_from_iso, tomorrow
from planner.area.views import get_regions_for_postcalcode
from planner.main.schedule import get_total_weight
from planner.main.schedule import APPOINTMENTS_PER_HALF_DAY

STANDARD_DAYS_AHEAD = 28

def space_available(calendar_id_string, appointment_form, appointment_id):
    # pylint: disable=E1101
    """ Assumes appointment_form's  is_valid was called and returned True"""
    if calendar_id_string:
        calendar_id = int(calendar_id_string)
        calendar = Calendar.objects.get(pk=calendar_id)
        existing_apps = calendar.active_appointments()
        kind = appointment_form.cleaned_data['kind']
        old_weight = 0
        if appointment_id != 'create':
            app = Appointment.actives.get(pk=int(appointment_id))
            old_weight = app.weight

        weight = get_total_weight(existing_apps, kind) - old_weight

        aw = int(appointment_form.cleaned_data['weight'])
        return weight + aw <= APPOINTMENTS_PER_HALF_DAY
    else:
        return False

@permission_required('main.callcenter')
def appointment_manipulation(request, appointment_id, customer_id, date_iso):
    # pylint: disable=E1101, R0912, R0915, R0204
    """ creates or edits an appointment and customer """
    free_space_errors = []
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
        carForm = CarForm()
        hidden_form = HiddenForm()
        appointment_form = AppointmentForm(instance=appointment)
        customer_form = CustomerForm(instance=appointment.customer)
    else:  # POST
        hidden_form = HiddenForm(request.POST)
        if hidden_form.is_valid():
            customer_id = hidden_form.cleaned_data['found_customer_id']
            if customer_id:
                appointment.customer = Customer.objects.get(pk=customer_id)
                logging.error("Customer known: %s", appointment.customer)
            else:
                logging.error("Customer unknown")
        else:
            raise NameError("Hiddenform should never be invalid")
        appointment_form = AppointmentForm(request.POST,
                                           instance=appointment)
        customer_form = CustomerForm(request.POST,
                                     instance=appointment.customer)
        carForm = CarForm(request.POST)
        free_space = request.POST.get('free_space', '')
        if free_space:
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
                    appointment_form.add_error('weight', _("No more space left"))
        else:
            free_space_errors = [_('Please select a date')]

    return render_to_response('appointment_manipulation.html',
                              {"appointmentForm": appointment_form,
                               "title": title,
                               "customerForm": customer_form,
                               "hiddenForm": hidden_form,
                               "date_iso": date_iso,
                               "calendar_id": calendar_id,
                               "carForm": carForm,
                               "free_space_errors": free_space_errors
                              },
                              context_instance=RequestContext(request))

def get_region_description(regions):
    if regions:
        return str([str(x.name) for x in regions])
    else:
        return _("Unknown")

@permission_required('main.callcenter')
def get_candidate_dates(request,
                        date_iso,
                        weight,
                        postalcode,
                        car_id,
                        kind,
                        calendar_id):
    # pylint: disable=R0913,W0613
    date = get_date_from_iso(date_iso)
    weight = int(weight)
    kind = int(kind)
    car_id = int(car_id)


    if postalcode != "-1":
        # normal pick-up case
        regions = get_regions_for_postcalcode(postalcode)
        region_code = get_region_description(regions)
    else:
        regions = None
        if car_id == -1:
            car_id = None

            region_code = _("Unrestricted")
        else:
            car = Car.objects.get(pk=car_id)
            region_code = " %s" % car.name


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
        available_dates = get_free_entries_with_extra_calendar(
            date,
            STANDARD_DAYS_AHEAD,
            regions,
            weight,
            kind,
            car_id,
            calendar)

    data = {'region': region_code, 'dates': available_dates}
    jsn = json.dumps(data)
    return HttpResponse(jsn, content_type='application/json')




@permission_required('main.callcenter')
def get_available_dates(request,
                        postalcode,
                        weight,
                        date_iso,
                        calendar_id,
                        unrestricted=False):
    # pylint: disable=R0913,W0613
    """ Returns a json object to fill the calendar choices component """
    logging.error("%s %s", postalcode, weight)
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
    jsn = json.dumps(data)
    return HttpResponse(jsn, content_type='application/json')


@permission_required('main.callcenter')
def get_customer(_, postalcode, number, addition):
    """ Returns a json object to fill the calendar choices component """
    customer_list = Customer.objects.filter(postcode__iexact=postalcode.capitalize(),
                                            number=number, additions=addition).all()
    if customer_list:
        customer = customer_list[0]
        data = {'name': customer.name,
                'found' : True,
                'address': customer.address,
                'town': customer.town,
                'phone': customer.phone,
                'id': customer.id,
                'email': customer.email}
    else:
        data = {'found': False}
    jsn = json.dumps(data)
    # logging.error("Customer JSON: %s for %s %s %s" % (jsn, postalcode, number, addition))
    return HttpResponse(jsn, content_type='application/json')


def logout_view(request):
    logout(request)
    return redirect('Overview', '')


@permission_required('main.callcenter')
def cancel_appointment(request, appointment_id):
    # pylint: disable=E1101
    appointment = Appointment.objects.get(pk=int(appointment_id))
    if request.method != 'POST':
        return render_to_response('appointment_cancel.html',
                                  {'object': appointment},
                                  context_instance=RequestContext(request)
                                 )
    else:
        appointment.status = 2
        appointment.save()
        return redirect('Overview', '')
