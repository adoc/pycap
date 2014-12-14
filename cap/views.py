"""
"""
import pytz
import collections

# put in own module
import datetime

from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import cap.util
import cap.models


# API views
@view_config(route_name="api_locations_get", renderer="json")
def api_locations_get(request):
    return (cap.models.DBSession
                .query(cap.models.Location)
                    .all())


@view_config(route_name="api_locations_post", renderer="json")
def api_locations_post(request, location=cap.models.Location()):
    """
    """
    date_format = request.registry.settings['date_format']
    local_tz = pytz.timezone(request.registry.settings['local_timezone'])
    # validate request params.
    params = request.json_body

    for key, val in params.items():
        if key == 'display_name':
            location.display_name = params['display_name']

        elif key == 'capacity':
            location.capacity = params['capacity']

        elif key.startswith("day_quantity"):
            #date = cap.util.get_utc_datetime(request,
            #        datetime.datetime.strptime(key.split('_')[-1], date_format))
            date = datetime.datetime.strptime(key.split('_')[-1], date_format).replace(tzinfo=pytz.utc)

            day_quantity = (
                cap.models.DBSession.query(cap.models.LocationDayQuantity)
                        .filter(cap.models.LocationDayQuantity.location==location)
                        .filter(cap.models.LocationDayQuantity.date==date)
                        .first() or 
                    cap.models.LocationDayQuantity())

            day_quantity.location = location
            day_quantity.date = date
            day_quantity.amount = val

    cap.models.DBSession.add(location)

    return True


@view_config(route_name="api_locations_get_byid", renderer="json")
def api_locations_get_byid(request):
    return (cap.models.DBSession
                .query(cap.models.Location)
                    .get(int(request.matchdict['id'])))


@view_config(route_name="api_locations_put", renderer="json")
def api_locations_put(request):
    return api_locations_post(request, location=api_locations_get_byid(request))


@view_config(route_name="api_days", renderer="json")
def days(request):
    return cap.util.get_days(request)


@view_config(route_name="home", renderer="templates/home.html.mako")
def home(request):
    """Shows a list of shops and their respective current capacities.
    """
    return {}


@view_config(route_name="locations_manage",
             renderer="templates/locations.manage.html.mako")
def locations_manage(request):
    """Shows a given shop and gives a field for entering number of cars
    for the next 7 days.
    """
    return {}


def location_update(request):
    """Same as location manage but adds a field for modifying the
    location capacity.
    """
    return {}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_cap_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

