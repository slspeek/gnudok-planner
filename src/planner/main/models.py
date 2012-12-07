from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime

class Customer(models.Model):
    """ Representa a customer """
    name = models.CharField(_('name'), max_length=30)
    postcode = models.CharField(_('postalcode'), max_length=14)
    number = models.CharField(_('number'), max_length=10)
    additions = models.CharField(_('additions'), max_length=10, blank=True)
    address = models.CharField(_('address'), max_length=120)
    town = models.CharField(_('town'), max_length=120)
    phone = models.CharField(_('phone'), max_length=30)
    email = models.EmailField(_('email'), max_length=120, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = (("postcode", "number", "additions"),)


def weekDayName(dayNumber):
    return [_("Monday"), _("Tuesday"),
            _("Wednesday"), _("Thursday"),
            _("Friday")][dayNumber - 1]


class TimeSlot(models.Model):
    CHOICES = ( (1,_("Monday")),
                (2,_("Tuesday")),
                (3, _("Wednesday")),
                (4, _("Thursday")),
                (5,_("Friday") ))
    day_of_week = models.IntegerField(choices=CHOICES)
    begin = models.FloatField()
    end = models.FloatField()

    def __str__(self):
        return u"%s :  %d - %d" % (weekDayName(self.day_of_week), self.begin, self.end)


class Region(models.Model):
    name = models.CharField(_('name'), max_length=120, unique=True)
    description = models.TextField(_('description'))

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(_('name'), max_length=20)
    
    def __str__(self):
        return self.name


class Rule(models.Model):
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))
    region = models.ForeignKey(Region, verbose_name=_('region'))
    active = models.BooleanField(default=True, verbose_name=_('active'))
    
    def __str__(self):
        return u"(%s, %s, %s)" % (str(self.car), str(self.timeslot), str(self.region))
    

class Calendar(models.Model):
    date = models.DateField(_('date'))
    car = models.ForeignKey(Car, verbose_name=_('car'))
    timeslot = models.ForeignKey(TimeSlot, verbose_name=_('timeslot'))
 

    def __str__(self):
        return u"(%s %s %s)" % (str(self.date), self.car, self.timeslot)
    
    class Meta:
        unique_together = (("date", "car", "timeslot"),)
        ordering = ['date', 'timeslot__begin']


class Appointment(models.Model):
    calendar = models.ForeignKey(Calendar, verbose_name=_('calendar'))
    customer = models.ForeignKey(Customer, verbose_name=_('customer'))
    employee = models.ForeignKey(User, verbose_name=_('employee'))
    KIND_CHOICES = ( (1,_("Delivery")),
                (2,_("Pick up")), )
    kind = models.IntegerField(_('kind'), choices=KIND_CHOICES, default=2)
    STATUS_CHOICES = ( (1,_("Normal")),
                (2,_("Deleted")), )
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    CHOICES = ( (1,_("Normal")),
                (2,_("Double")),
                (3, _("Tripel")),
                (4, _("Entire half-day")),
                 )
    weight = models.IntegerField(_('weight'), choices=CHOICES, default=1)
    stuff = models.TextField(_('stuff'))
    notes = models.TextField(_('notes'), blank=True)
    created = models.DateTimeField(_("created"), default=lambda:datetime.datetime.now())

    def __str__(self):
        return self.customer.name + ", " + self.stuff
    
    class Meta:
        ordering = ['customer__postcode']
