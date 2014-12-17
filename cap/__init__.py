import pyramid.config
import pyramid.authentication
import pyramid.authorization
import sqlalchemy

import cap.models
import cap.auth


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Set up authentication and authorization.
    authn_policy = pyramid.authentication.AuthTktAuthenticationPolicy(
                        settings['auth.secret'],
                        callback=cap.auth.groupfinder)
    authz_policy = pyramid.authorization.ACLAuthorizationPolicy()

    config = pyramid.config.Configurator(
                        settings=settings,
                        authentication_policy=authn_policy,
                        authorization_policy=authz_policy,
                        root_factory=cap.auth.RootFactory)

    engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    cap.models.DBSession.configure(bind=engine)
    cap.models.Base.metadata.bind = engine
    cap.models.init_models(settings)

    config.add_static_view('static', 'static',
                            cache_max_age=int(settings['cache_max_age']))

    # Auth routes.
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # HTML view routes.
    config.add_route('home', '/')
    config.add_route('locations_manage', '/locations/edit')
    config.add_route('locations_view', '/locations')
    config.add_route('location_view', '/{location_name}')

    # API routes.
    config.add_route('api_days', '/api/v1/days')
    config.add_route('api_locations_get', '/api/v1/locations',
                        request_method=("GET",))
    config.add_route('api_locations_post', '/api/v1/locations',
                        request_method=("POST",))
    config.add_route('api_locations_get_byid', '/api/v1/locations/{id}',
                        request_method=("GET",))
    config.add_route('api_locations_put', '/api/v1/locations/{id}',
                        request_method=("PUT",))

    config.scan()
    return config.make_wsgi_app()
