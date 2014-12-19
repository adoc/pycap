"""
"""

import collections
import datetime
import pytz
import sqlalchemy.orm.exc

import pyramid.view
import pyramid.security

import cap.util
import cap.models


# API views

@pyramid.view.view_config(route_name="api_locations_get", renderer="json",
                            permission="view")
def api_locations_get(request):
    return (cap.models.DBSession
                    .query(cap.models.Location)
                        .all())


@pyramid.view.view_config(route_name="api_locations_post", renderer="json")
def api_locations_post(request, location=cap.models.Location()):
    """
    """
    date_format = request.registry.settings['date_format']
    local_tz = pytz.timezone(request.registry.settings['local_timezone'])
    
    # TODO: validate request params.
    params = request.json_body

    for key, val in params.items():
        if key == 'display_name': # Location `display_name` has been updated.
            location.display_name = params['display_name']

        elif key == 'capacity': # Location `capacity` has been updated.
            location.capacity = params['capacity']

        elif key == 'day_quantities': # Location `day_quantities` have
            for day_quantity in val:  # been updated.
                if ('date' in day_quantity and
                        'amount' in day_quantity and
                        day_quantity['amount'] >= 0):
                    amount = day_quantity['amount']
                    date = (datetime.datetime.strptime(day_quantity['date'],
                                                        date_format)
                                .replace(tzinfo=local_tz))
                    try:
                        day_quantity_record = (cap.models.DBSession
                          .query(cap.models.LocationDayQuantity)
                              .filter(
                                cap.models.LocationDayQuantity.location==location)
                              .filter(
                                cap.models.LocationDayQuantity.date==date)
                              .one())
                    except sqlalchemy.orm.exc.NoResultFound:
                        day_quantity_record = cap.models.LocationDayQuantity()

                    day_quantity_record.location = location
                    day_quantity_record.date = date
                    day_quantity_record.amount = amount

    cap.models.DBSession.add(location)

    return True


@pyramid.view.view_config(route_name="api_locations_put", renderer="json")
def api_locations_put(request):
    return api_locations_post(request, location=api_locations_get_byid(request))


@pyramid.view.view_config(route_name="api_locations_get_byid", renderer="json")
def api_locations_get_byid(request):
    return (cap.models.DBSession
                .query(cap.models.Location)
                    .get(int(request.matchdict['id'])))


@pyramid.view.view_config(route_name="api_days", renderer="json")
def api_days(request):
    return cap.util.get_days(request)


@pyramid.view.view_config(route_name="api_location_test", renderer="json",
                            permission="edit")
def api_location_test(request):
    # print(request.context)
    return request.context


# HTML Views

@pyramid.view.view_config(route_name="locations_manage",
            permission='edit',
            renderer="templates/locations.manage.html.mako")
def locations_manage(request):
    """Shows a given shop and gives a field for entering number of cars
    for the next 7 days.
    """
    return {}


@pyramid.view.view_config(route_name="home",
            permission='view',
            renderer="templates/locations.view.html.mako")
def home(request):
    """Shows a given shop and gives a field for entering number of cars
    for the next 7 days.
    """
    return {}