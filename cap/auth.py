"""
Excerpts pulled from
https://github.com/mmerickel/pyramid_auth_demo/blob/master/2.object_security/demo.py
"""

import os
import hashlib

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.orm.exc

import pyramid.security
import pyramid.view
import pyramid.httpexceptions


import cap.models


class UserGroup(cap.models.Base):
    __tablename__ = "usersgroups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    userid = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    groupid = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("groups.id"))


class Group(cap.models.Base):
    __tablename__ = "groups"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=64), unique=True)

    users = sqlalchemy.orm.relationship("User", 
                                        secondary=UserGroup.__table__)


class User(cap.models.Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=64), unique=True,
                                 index=True)
    passhash = sqlalchemy.Column(sqlalchemy.LargeBinary(length=64))
    _salt = sqlalchemy.Column('salt', sqlalchemy.LargeBinary(length=8),
                                default=lambda: os.urandom(8))

    groups = sqlalchemy.orm.relationship(Group,
                                         secondary=UserGroup.__table__)

    @property
    def salt(self):
        if not self._salt:
            self._salt = os.urandom(8)
        return self._salt

    @property
    def password(self):
        raise Exception("Cannot get a password.")

    @password.setter
    def password(self, value):
        hash = hashlib.sha256(self.salt)
        hash.update(value.encode())
        self.passhash = hash.digest()

    def check_password(self, password):
        hash = hashlib.sha256(self.salt)
        hash.update(password.encode())
        challenge_hash = hash.digest()
        return self.passhash == challenge_hash


class RootFactory:
    """Root factory for this Pyramid application."""
    __acl__ = [(pyramid.security.Allow, 'g:admins', pyramid.security.ALL_PERMISSIONS),
                (pyramid.security.Allow, 'g:managers', 'edit'),
                (pyramid.security.Allow, 'g:managers', 'view'),
                (pyramid.security.Allow, 'g:users', 'view')]

    def __init__(self, request):
        self.request = request


class ApiFactory(RootFactory):
    pass


class LocationFactory(ApiFactory):
    """ """

    def __getitem__(self, id):
        """Accessed via "traversal" """
        location = cap.models.DBSession.query(cap.models.Location).get(id)
        if location:
            location.__parent__ = self
            return location


def get_user(request, user_name):
    try:
        return cap.models.DBSession.query(User).filter(User.name==user_name).one()
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def get_this_user(request):
    user_name= pyramid.security.unauthenticated_userid(request)
    if user_name:
        return get_user(request, user_name)


def get_groups(user_name, request):    # Yes, user_name first unfortunately.
    user = get_user(request, user_name)
    if user:
        return ['g:%s' % g.name for g in user.groups]


@pyramid.view.forbidden_view_config()
def forbidden_view(request):
    """Return HTTPUnauthorized when user is logged in but unauthorized,
    redirect to 'login' route if no user is logged in.
    """
    # do not allow a user to login if they are already logged in
    if pyramid.security.authenticated_userid(request):
        return pyramid.httpexceptions.HTTPUnauthorized()

    return pyramid.httpexceptions.HTTPFound(location=
                request.route_url('login', _query=(('next', request.path),)))


@pyramid.view.forbidden_view_config(containment=ApiFactory)
def api_forbidden_view(request):
    """Return HTTPUnauthorized when unauthorized API request is
    made."""
    return pyramid.httpexceptions.HTTPUnauthorized()


@pyramid.view.view_config(route_name='login',
                            renderer='templates/login.html.mako')
def login_view(request):
    if 'submit' in request.POST:
        next = request.params.get('next') or request.route_url('home')
        user_name = request.POST.get('login', '')
        passwd = request.POST.get('password', '')

        user = get_user(request, user_name)
        if user and user.check_password(passwd):
            headers = pyramid.security.remember(request, user_name)
            return pyramid.httpexceptions.HTTPFound(location=next, headers=headers)
        else:
            return {'failed': True}
    return {}


@pyramid.view.view_config(route_name='logout')
def logout_view(request):
    headers = pyramid.security.forget(request)
    loc = request.route_url('home')
    return pyramid.httpexceptions.HTTPFound(location=loc, headers=headers)