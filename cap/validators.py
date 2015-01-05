import re
import formencode

import cap.util


alpha = re.compile('[\W_]+')


def init_schema(settings):
    global DayQuantitySchema
    global LocationSchema
    global UserSchema

    formencode.validators.datetime_now = (lambda *a:
                                    cap.util.get_localized_datetime(settings))

    # Convert from date format to formencode's convention.
    month_style = alpha.sub('', settings['date_format']).lower()


    class DayQuantitySchema(formencode.schema.Schema):
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = False

        date = formencode.compound.Pipe(validtors=[
                        formencode.validators.DateConverter(
                                                    month_style=month_style),
                        formencode.validators.DateValidator(
                                                    today_or_after=True)])
        amount = formencode.validators.Int(min=-1)


    class LocationSchema(formencode.schema.Schema):
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = False

        display_name = formencode.validators.String(min=4, max=32)
        capacity = formencode.validators.Int(min=0)
        day_quantities = formencode.foreach.ForEach(DayQuantitySchema())


    class UserSchema(formencode.schema.Schema):
        allow_extra_fields = True
        filter_extra_fields = True
        ignore_key_missing = True

        name = formencode.validators.String(min=3, max=32)

        password = formencode.validators.String(min=4, max=32)
        password_confirm = formencode.validators.String(min=4, max=32)

        chained_validators = [formencode.validators.FieldsMatch(
                                 'password', 'password_confirm')]