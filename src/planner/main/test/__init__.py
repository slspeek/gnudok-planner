from planner.main.models import Car, TimeSlot, Region, Rule, Customer, Appointment, Calendar
import factory
from django.contrib.auth.models import User
import datetime


class CarFactory(factory.Factory):
    FACTORY_FOR = Car
    
    name = "Open source tractor"
    
    
class TimeSlotFactory(factory.Factory):
    FACTORY_FOR = TimeSlot

    day_of_week = 1
    begin = 13
    end = 17


class RegionFactory(factory.Factory):
    FACTORY_FOR = Region

    name = "Groot Oost"

class RuleFactory(factory.Factory):
    FACTORY_FOR = Rule
    
    car = factory.SubFactory(CarFactory)
    region = factory.SubFactory(RegionFactory)
    timeslot = factory.SubFactory(TimeSlotFactory)
    
    

class CustomerFactory(factory.Factory):
    FACTORY_FOR = Customer

    name = "Willem Knaap"
    address = "Grachtengordel 1"
    town = "Juinen"
    postcode = "1469 SH"
    phone = "020-6164590"
    email = "wk@example.com"


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = "nancy"
    password = "nancy-secret"


class CalendarFactory(factory.Factory):
    FACTORY_FOR = Calendar

    date = datetime.date(2012, 10, 29)
    timeslot = factory.SubFactory(TimeSlotFactory)
    car = factory.SubFactory(CarFactory)
    #region = factory.SubFactory(RegionFactory)


class AppointmentFactory(factory.Factory):
    FACTORY_FOR = Appointment

    calendar = factory.SubFactory(CalendarFactory)
    customer = factory.SubFactory(CustomerFactory)
    employee = factory.SubFactory(UserFactory)
    stuff = "Gold, Platina and lots of Silver"
    notes = "Bring boxes"
    created = datetime.datetime.now()
