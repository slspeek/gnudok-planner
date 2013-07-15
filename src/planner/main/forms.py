'''
Created on 15 nov. 2012

@author: steven
'''
from __future__ import absolute_import
from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import Appointment, Customer, Region, Car
from django.forms.forms import Form
from django.utils.translation import ugettext_lazy as _


class CalendarSearchForm(forms.Form):
    name = forms.CharField(label=_('name'), required=False)
    postcode = forms.CharField(label=_('postalcode'), required=False)
    street = forms.CharField(label=_('street'), required=False)
    town = forms.CharField(label=_('town'), required=False)
    date = forms.DateField(label=_('date'),
                           required=False,
                           widget=BootstrapDateInput())
    stuff = forms.CharField(label=_('stuff'), required=False)
    include_past = forms.BooleanField(label=_('include past'), required=False)
    include_cancelled = forms.BooleanField(label=_('include cancelled'), required=False)


class DatePickForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput())


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ("kind", "weight", "stuff", "notes")


class CustomerForm(ModelForm):
    class Meta:
        model = Customer


class HiddenForm(forms.Form):
    found_customer_id = forms.IntegerField(widget=forms.HiddenInput(),
                                           required=False)


class EmployeeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class EmployeeChooseForm(Form):
    queryset = User.objects.filter(groups__name='Callcenter')\
        .filter(is_active=True)\
        .order_by('first_name')
    employee = EmployeeModelChoiceField(label=_('employee'), queryset=queryset)
    
class CarModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class CarForm(Form):
    queryset = Car.objects.all()
    car = CarModelChoiceField(label=_('car'), queryset=queryset)
