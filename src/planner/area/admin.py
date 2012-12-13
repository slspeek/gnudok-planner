'''
Admin configuration
'''
from __future__ import absolute_import
from .models import Interval
from planner.main.models import Region
from django.contrib import admin

admin.site.register(Interval)
