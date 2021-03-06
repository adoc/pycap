import os
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

    def sstatic_url(request, path_key, *path):
        """Serve a static URL from a path in the settings (ini).
        """
        return request.static_url(os.path.join(settings[path_key], *path))

    def sstatic_path(request, path_key, *path):
        """
        """
        return request.static_path(os.path.join(settings[path_key], *path))

    config.add_request_method(sstatic_url)
    config.add_request_method(sstatic_path)

    config.add_request_method(cap.auth.get_this_user, 'this_user', reify=True)

    config.add_static_view(name='static', path=settings['static_dir'],
                            cache_max_age=int(settings['cache_max_age']))

    def js_view(request):
        request.response.content_type = 'application/javascript'
        return {}

    config.add_route('config.js', '/config.js')
    config.add_route('common.js', '/common.js')
    config.add_view(js_view, route_name='config.js',
                    renderer='templates/config.js.mako',
                    http_cache=int(settings['cache_max_age']))
    config.add_view(js_view, route_name='common.js',
                    renderer='templates/common.js.mako',
                    http_cache=int(settings['cache_max_age']))

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
