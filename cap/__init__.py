from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    #config.include('pyramid_chameleon')
    config.add_static_view('static', 'static',
                            cache_max_age=int(settings['cache_max_age']))

    config.add_route('home', '/')
    config.add_route('locations_manage', '/locations')


    config.add_route('api_locations_get', '/api/v1/locations',
                        request_method=("GET",))
    config.add_route('api_locations_post', '/api/v1/locations',
                        request_method=("POST",))
    config.add_route('api_locations_get_byid', '/api/v1/locations/{id}',
                        request_method=("GET",))
    config.add_route('api_locations_put', '/api/v1/locations/{id}',
                        request_method=("PUT",))



    config.add_route('api_days', '/api/v1/days')


    config.scan()
    return config.make_wsgi_app()
