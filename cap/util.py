import datetime
import pytz


def get_localized_datetime(request_or_settings):
    """Get the current UTC and return the localized datetime based on
    the timezone set with "local_timezone" in the config file.
    TODO: Ultimately this will use the location's timezone.
    """
    if hasattr(request_or_settings, 'registry'):
        settings = request_or_settings.registry.settings
    else:
        settings = request_or_settings

    local_tz = pytz.timezone(settings['local_timezone'])
    now_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    return now_utc.astimezone(local_tz)


def get_utc_datetime(request, dt):
    local_tz = pytz.timezone(request.registry.settings['local_timezone'])
    dt = dt.replace(tzinfo=local_tz)
    return dt.astimezone(pytz.utc)


def g(dt):
    local_tz = pytz.timezone("US/Pacific")
    dt = dt.replace(tzinfo=local_tz)
    return dt.astimezone(pytz.utc)


def get_days(request):
    """Get today (localized) and the next 6 days.
    Return a list of nested tuples.
    (weekday_number, weekday_name, weekday_abbreviation, date_string).
    """
    now = get_localized_datetime(request)
    format = request.registry.settings['date_format']
    def gen_days():
        for day_offset in range(1, 11):
            delta = datetime.timedelta(days=day_offset-1) # For calculating the date.
            day = (now + delta)
            yield {'day_num': int(day.strftime('%w')),
                    'day_name': day.strftime('%A'),
                    'day_abbr': day.strftime('%a'),
                    'date':day.strftime(format)}
    return list(gen_days())