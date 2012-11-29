from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """ Representa a customer """
    name = models.CharField(max_length=80)
    postcode = models.CharField(max_length=14)
    number = models.CharField(max_length=10)
    additions = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=120)
    town = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.EmailField(max_length=120, blank=True)

    def __str__(self):
        return self.name


def weekDayName(dayNumber):
    return ["Monday", "Tuesday",
            "Wednesday", "Thursday",
            "Friday"][dayNumber - 1]


class TimeSlot(models.Model):
    day_of_week = models.IntegerField()
    begin = models.FloatField()
    end = models.FloatField()

    def __str__(self):
        return "%s :  %d - %d" % (weekDayName(self.day_of_week), self.begin, self.end)


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField()
    timeslots = models.ManyToManyField(TimeSlot)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Rule(models.Model):
    car = models.ForeignKey(Car)
    timeslot = models.ForeignKey(TimeSlot)
    region = models.ForeignKey(Region)
    def __str__(self):
        return "(%s, %s, %s)" % (str(self.car), str(self.timeslot), str(self.region))
    

class Calendar(models.Model):
    date = models.DateField()
    car = models.ForeignKey(Car)
    timeslot = models.ForeignKey(TimeSlot)

    def __str__(self):
        return "(%s %s %s)" % (str(self.date), self.car, self.timeslot)
    
    class Meta:
        unique_together = (("date", "car", "timeslot"),)


class Appointment(models.Model):
    calendar = models.ForeignKey(Calendar)
    customer = models.ForeignKey(Customer)
    employee = models.ForeignKey(User)
    stuff = models.TextField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.customer.name + ", " + self.stuff
    
    class Meta:
        ordering = ['customer__postcode']
