'''
Created on 15 nov. 2012

@author: steven
'''
from __future__ import absolute_import
from django import forms
from bootstrap_toolkit.widgets import BootstrapDateInput
from django.forms.models import ModelForm
from .models import Appointment, Customer, Region
from django.forms.forms import Form

class CalendarSearchForm(forms.Form):
    name = forms.CharField(required=False)
    #postcode = forms.CharField(required=False)
    #date = forms.DateField(required=False)
   
class DatePickForm(forms.Form):
    date = forms.DateField(widget=BootstrapDateInput())
    
class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ("stuff", "notes")
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer

class HiddenForm(forms.Form):
    timeslot_id = forms.IntegerField(widget=forms.HiddenInput())
    car_id = forms.IntegerField(widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.HiddenInput())
    weight = forms.IntegerField(widget=forms.HiddenInput())
    
class RegionChooseForm(Form):
    region = forms.ModelChoiceField(queryset=Region.objects.all()) 
    CHOICES = ( (1,"Normal"),
                (2,"Double"),
                (3, "Tripel"),
                (4, "Entire half-day"),
                 )
    weight = forms.ChoiceField(choices=CHOICES, initial=1)
