import factory
from ..models import Interval


class IntervalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Interval
