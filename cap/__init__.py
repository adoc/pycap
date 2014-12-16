from pyramid.config import Configurator
from sqlalchemy import engine_from_config

import cap.models


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    cap.models.DBSession.configure(bind=engine)
    cap.models.Base.metadata.bind = engine
    cap.models.init_models(settings)
    config = Configurator(settings=settings)

    #config.include('pyramid_chameleon')
    config.add_static_view('static', 'static',
                            cache_max_age=int(settings['cache_max_age']))

    # HTML view routes.
    config.add_route('home', '/')
    config.add_route('locations_manage', '/manage')
    config.add_route('locations_view', '/locations')
    config.add_route('location_view', '/{location_name}')

    # API routes.
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
