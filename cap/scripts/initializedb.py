import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

import cap.models


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    cap.models.DBSession.configure(bind=engine)
    cap.models.init_models(settings)
    cap.models.Base.metadata.drop_all(engine)
    cap.models.Base.metadata.create_all(engine)
    


    with transaction.manager:
        cap.models.DBSession.add(cap.models.Location(display_name='Alhambra'))
        cap.models.DBSession.add(cap.models.Location(display_name='Montebello'))
        cap.models.DBSession.add(cap.models.Location(display_name='La Puente'))
        cap.models.DBSession.add(cap.models.Location(display_name='Pasadena'))
        cap.models.DBSession.add(cap.models.Location(display_name='Duarte'))
        cap.models.DBSession.add(cap.models.Location(display_name='Perris'))
        cap.models.DBSession.add(cap.models.Location(display_name='Loma Linda'))
        cap.models.DBSession.add(cap.models.Location(display_name='Corona'))
        cap.models.DBSession.add(cap.models.Location(display_name='Riverside'))
        cap.models.DBSession.add(cap.models.Location(display_name='Fontana'))
        cap.models.DBSession.add(cap.models.Location(display_name='West Covina'))
        cap.models.DBSession.add(cap.models.Location(display_name='Rosemead'))
        cap.models.DBSession.add(cap.models.Location(display_name='Glendora'))
        cap.models.DBSession.add(cap.models.Location(display_name='Ontario'))
