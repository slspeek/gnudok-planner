'''
Created on 15 nov. 2012

@author: steven
'''
from __future__ import absolute_import
from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import Appointment, Customer, Region
from django.forms.forms import Form
from django.utils.translation import ugettext_lazy as _

class CalendarSearchForm(forms.Form):
    name = forms.CharField(label=_('name'), required=False)
    #postcode = forms.CharField(required=False)
    #date = forms.DateField(required=False)
   
class DatePickForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput())
    
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ("stuff", "notes")
        
class BigAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ("weight", "stuff", "notes")
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer

class HiddenForm(forms.Form):
    found_customer_id = forms.IntegerField(widget=forms.HiddenInput())
    
    
class RegionChooseForm(Form):
    region = forms.ModelChoiceField(label=_('region'), queryset=Region.objects.all()) 
    CHOICES = ( (1,_("Normal")),
                (2,_("Double")),
                (3, _("Tripel")),
                (4, _("Entire half-day")),
                 )
    weight = forms.ChoiceField(label=_('weight'), choices=CHOICES, initial=1)
    
class EmployeeChooseForm(Form):
    employee = forms.ModelChoiceField(label=_('employee'), queryset=User.objects.all()) 
    