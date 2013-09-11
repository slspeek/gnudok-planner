import datetime
from django.contrib.auth.decorators import user_passes_test


def tomorrow():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    return (today + one_day).strftime('%Y%m%d')

def today():
    today = datetime.date.today()
    return today.strftime('%Y%m%d')


def get_date_from_iso(iso_date):
    """ Returns a date object corresponding to the given iso-date string. """
    return datetime.datetime.strptime(iso_date, '%Y%m%d').date()


def to_iso(date):
    return date.strftime('%Y%m%d')


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


def float_to_time(number):
    import math
    frac = math.modf(number)[0]
    minutes = ("%.2f" % (frac * (60.0 / 100.0)))[2:]
    whole = int(math.modf(number)[1])
    return "%d:%s" % (whole, minutes)
