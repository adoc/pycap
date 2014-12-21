import datetime
import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import sqlalchemy.ext.hybrid
import zope.sqlalchemy
import pyramid.security
import pytz
import cap.util

from sqlalchemy.sql.expression import func


DBSession = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker(
                    extension=zope.sqlalchemy.ZopeTransactionExtension()))
Base = sqlalchemy.ext.declarative.declarative_base()


def init_models(settings, UserModel):
    """To be run during application initialization. This allows for the passing
    of config options.
    """
    global Location
    global LocationDayQuantity

    date_format = settings['date_format']

    class EpochDays(sqlalchemy.types.TypeDecorator):
        """
        http://docs.sqlalchemy.org/en/rel_0_9/core/types.html#sqlalchemy.types.TypeDecorator
        """
        impl = sqlalchemy.types.Integer
        epoch = datetime.datetime(1970, 1, 1).replace(
                            tzinfo=pytz.timezone(settings['local_timezone']))

        def process_bind_param(self, value, dialect):
            return (value - self.epoch).days

        def process_result_value(self, value, dialect):
            return self.epoch + datetime.timedelta(days=value)

    class Location(Base):
        @property
        def __acl__(self):
            if self.owner:
                return [
                    (pyramid.security.Allow, 'g:admins', pyramid.security.ALL_PERMISSIONS),
                    (pyramid.security.Allow, 'g:managers', pyramid.security.ALL_PERMISSIONS),
                    (pyramid.security.Allow, 'g:users', 'view'),
                    (pyramid.security.Allow, self.owner.name, 'edit')
                ]
            else:
                return []

        __tablename__ = 'locations'
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        display_name = sqlalchemy.Column(sqlalchemy.String(64), index=True,
                                            unique=True)
        capacity = sqlalchemy.Column(sqlalchemy.Integer, default=0)

        owner_userid = sqlalchemy.Column(sqlalchemy.Integer,
                                         sqlalchemy.ForeignKey(UserModel.id))

        owner = sqlalchemy.orm.relationship(UserModel, backref="locations")

        dyn_day_quantities = sqlalchemy.orm.relationship("LocationDayQuantity",
                                                        lazy="dynamic")

        @sqlalchemy.ext.hybrid.hybrid_property
        def name(self):
            """Name function to lowercase and replace spaces with
            underscore."""
            return self.display_name.lower().replace(' ', '_')

        @name.expression
        def name(cls):
            """SQL representation of the `name` function."""
            return func.replace(func.lower(cls.display_name), ' ', '_')

        def __json__(self, request):
            return {
                'id': self.id,
                'display_name': self.display_name,
                'capacity': self.capacity,
                'day_quantities': (
                    self.dyn_day_quantities.filter(
                                LocationDayQuantity.date >=
                                    cap.util.get_localized_datetime(request))
                                .order_by(LocationDayQuantity.date.asc())
                                .all()),
                'perm_edit': isinstance(request.has_permission('edit', self),
                                        pyramid.security.ACLAllowed),
                'perm_manage': isinstance(request.has_permission('manage', self),
                                        pyramid.security.ACLAllowed)
            }

    class LocationDayQuantity(Base):
        __tablename__ = 'location_amounts'
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        date = sqlalchemy.Column(EpochDays, nullable=False)
        location_id = sqlalchemy.Column(sqlalchemy.Integer,
                        sqlalchemy.ForeignKey(Location.id), nullable=False)
        location = sqlalchemy.orm.relationship(Location, backref="day_quantities")
        amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

        def __json__(self, request):
            return {
                'date': self.date.strftime(date_format),
                'amount': self.amount
            }