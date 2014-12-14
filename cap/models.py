import datetime
import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import zope.sqlalchemy

import pytz
import cap.util


DBSession = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker(
                    extension=zope.sqlalchemy.ZopeTransactionExtension()))
Base = sqlalchemy.ext.declarative.declarative_base()


def init_models(settings):
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
        __tablename__ = 'locations'
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        display_name = sqlalchemy.Column(sqlalchemy.String(64), index=True,
                                            unique=True)
        capacity = sqlalchemy.Column(sqlalchemy.Integer, default=0)

        dyn_day_quantities = sqlalchemy.orm.relationship("LocationDayQuantity",
                                                        lazy="dynamic")

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
                                .all())
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