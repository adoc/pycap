import pyramid.config
import pyramid.authentication
import pyramid.authorization
import sqlalchemy

import cap.models
import cap.validators
import cap.auth



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    # Set up authentication and authorization.
    authn_policy = pyramid.authentication.AuthTktAuthenticationPolicy(
                        settings['auth.secret'],
                        callback=cap.auth.get_groups)
    authz_policy = pyramid.authorization.ACLAuthorizationPolicy()

    config = pyramid.config.Configurator(
                        settings=settings,
                        authentication_policy=authn_policy,
                        authorization_policy=authz_policy,
                        root_factory=cap.auth.RootFactory)

    engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    cap.models.DBSession.configure(bind=engine)
    cap.models.Base.metadata.bind = engine
    cap.models.init_models(settings, cap.auth.User)
    cap.validators.init_schema(settings)

    config.add_request_method(cap.auth.get_this_user, 'this_user', reify=True)

    config.add_static_view('static', 'static',
                            cache_max_age=int(settings['cache_max_age']))

    # If updating routes, make sure to update the `api_get_routes` view
    #   as well.

    # HTML view routes.
    config.add_route('home', '/', factory=cap.auth.RootFactory)
    config.add_route('users', '/users', factory=cap.auth.RootFactory)

    # Auth routes.
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # API routes.
    #   Locations
    config.add_route('api_days', '/api/v1/days',
                        factory=cap.auth.ApiFactory)
    config.add_route('api_locations_get', '/api/v1/locations',
                        request_method=("GET",),
                        factory=cap.auth.ApiFactory)
    config.add_route('api_location_get', '/api/v1/locations/{id}',
                        request_method=("GET",),
                        factory=cap.auth.LocationFactory, traverse="/{id}")
    config.add_route('api_location_update', '/api/v1/locations/{id}',
                        request_method=("PUT",),
                        factory=cap.auth.LocationFactory, traverse="/{id}")
    # Current no POST (Cannot add Locations.)
    
    #   Users
    config.add_route('api_users_get', '/api/v1/users',
                        request_method=("GET",),
                        factory=cap.auth.UsersFactory)
    config.add_route('api_user_get', '/api/v1/users/{id}',
                        request_method=("GET",),
                        factory=cap.auth.UsersFactory, traverse="/{id}")
    config.add_route('api_user_update', '/api/v1/users/{id}',
                        request_method=("PUT",),
                        factory=cap.auth.UsersFactory, traverse="/{id}")

    config.scan()
    return config.make_wsgi_app()
