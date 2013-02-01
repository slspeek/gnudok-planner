from django.db import models
from django.utils.translation import ugettext_lazy as _
from planner.main.models import Region


class Interval(models.Model):
    begin = models.CharField(_('begin'), max_length=8)
    end = models.CharField(_('end'), max_length=8)
    region = models.ForeignKey(Region, verbose_name=_('region'))

    def __str__(self):
        return "(%s - %s) in %s" % (self.begin, self.end, self.region.name)
