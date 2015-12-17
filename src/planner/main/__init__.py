import datetime

def tomorrow():
    t = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    return (t + one_day).strftime('%Y%m%d')

def today():
    t = datetime.date.today()
    return t.strftime('%Y%m%d')


def get_date_from_iso(iso_date):
    """ Returns a date object corresponding to the given iso-date string. """
    return datetime.datetime.strptime(iso_date, '%Y%m%d').date()


def to_iso(date):
    return date.strftime('%Y%m%d')


def float_to_time(number):
    import math
    frac = math.modf(number)[0]
    minutes = ("%.2f" % (frac * (60.0 / 100.0)))[2:]
    whole = int(math.modf(number)[1])
    return "%d:%s" % (whole, minutes)
