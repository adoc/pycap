"""
Excerpts pulled from
https://github.com/mmerickel/pyramid_auth_demo/blob/master/2.object_security/demo.py
"""
import pyramid.security
import pyramid.view
import pyramid.httpexceptions


class User(object):
    @property
    def __acl__(self):
        return [(Allow, self.username, 'view')]

    def __init__(self, username, password, groups=None):
        self.username = username
        self.password = password
        self.groups = groups or []

    def check_password(self, password):
        return self.password == password


class RootFactory(object):
    """Root factory for this Pyramid application."""
    __acl__ = [(pyramid.security.Allow, 'g:admins', pyramid.security.ALL_PERMISSIONS),
                (pyramid.security.Allow, 'g:managers', 'manager'),
                (pyramid.security.Allow, 'g:managers', 'user'),
                (pyramid.security.Allow, 'g:users', 'user')]

    def __init__(self, request):
        self.request = request


USERS = {
    "admin": User("admin", "admin111", ['admins']),
    "manager": User("manager", "manager222", ['managers']),
    "user": User("user", "user333", ['users'])
}


def groupfinder(userid, request):
    user = USERS.get(userid)
    if user:
        return ['g:%s' % g for g in user.groups]


@pyramid.view.forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if pyramid.security.authenticated_userid(request):
        return pyramid.httpexceptions.HTTPForbidden()

    return pyramid.httpexceptions.HTTPFound(location=
                request.route_url('login', _query=(('next', request.path),)))


@pyramid.view.view_config(route_name='login',
                            renderer='templates/login.html.mako')
def login_view(request):
    if 'submit' in request.POST:
        next = request.params.get('next') or request.route_url('home')
        login = request.POST.get('login', '')
        passwd = request.POST.get('password', '')

        user = USERS.get(login, None)
        if user and user.check_password(passwd):
            headers = pyramid.security.remember(request, login)
            return pyramid.httpexceptions.HTTPFound(location=next, headers=headers)
        else:
            return {'failed': True}
    return {}


@pyramid.view.view_config(route_name='logout')
def logout_view(request):
    headers = pyramid.security.forget(request)
    loc = request.route_url('home')
    return pyramid.httpexceptions.HTTPFound(location=loc, headers=headers)