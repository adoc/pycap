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
import cap.auth


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
    cap.models.init_models(settings, cap.auth.User)
    cap.models.Base.metadata.drop_all(engine)
    cap.models.Base.metadata.create_all(engine)


    with transaction.manager:
        # Add groups
        admins = cap.auth.Group(name="admins")
        managers = cap.auth.Group(name="managers")
        users = cap.auth.Group(name="users")
        cap.models.DBSession.add(admins)
        cap.models.DBSession.add(managers)
        cap.models.DBSession.add(users)

        # Add users
        cap.models.DBSession.add(cap.auth.User(name="admin", password="admin",
                                                groups=[admins]))
        cap.models.DBSession.add(cap.auth.User(name="manager",
                                                password="manager",
                                                groups=[managers]))

        alhambra = cap.auth.User(name="alhambra", password="alhambra",
                                groups=[users])
        montebello = cap.auth.User(name="montebello", password="montebello",
                                groups=[users])
        lapuente = cap.auth.User(name="lapuente", password="lapuente",
                                groups=[users])
        duarte = cap.auth.User(name="duarte", password="duarte",
                                groups=[users])
        perris = cap.auth.User(name="perris", password="perris",
                                groups=[users])
        lomalinda = cap.auth.User(name="lomalinda", password="lomalinda",
                                groups=[users])
        corona = cap.auth.User(name="corona", password="corona",
                                groups=[users])
        fontana = cap.auth.User(name="fontana", password="fontana",
                                groups=[users])
        westcovina = cap.auth.User(name="westcovina", password="westcovina",
                                groups=[users])
        rosemead = cap.auth.User(name="rosemead", password="rosemead",
                                groups=[users])
        glendora = cap.auth.User(name="glendora", password="glendora",
                                groups=[users])
        ontario = cap.auth.User(name="ontario", password="ontario",
                                groups=[users])

        # Add locations
        cap.models.DBSession.add(cap.models.Location(display_name='Alhambra',
                                                     owner=alhambra))
        cap.models.DBSession.add(cap.models.Location(display_name='Montebello',
                                                     owner=montebello))
        cap.models.DBSession.add(cap.models.Location(display_name='La Puente',
                                                     owner=lapuente))
        cap.models.DBSession.add(cap.models.Location(display_name='Duarte',
                                                     owner=duarte))
        cap.models.DBSession.add(cap.models.Location(display_name='Perris',
                                                     owner=perris))
        cap.models.DBSession.add(cap.models.Location(display_name='Loma Linda',
                                                     owner=lomalinda))
        cap.models.DBSession.add(cap.models.Location(display_name='Corona',
                                                     owner=corona))
        cap.models.DBSession.add(cap.models.Location(display_name='Fontana',
                                                     owner=fontana))
        cap.models.DBSession.add(cap.models.Location(display_name='West Covina',
                                                     owner=westcovina))
        cap.models.DBSession.add(cap.models.Location(display_name='Rosemead',
                                                     owner=rosemead))
        cap.models.DBSession.add(cap.models.Location(display_name='Glendora',
                                                     owner=glendora))
        cap.models.DBSession.add(cap.models.Location(display_name='Ontario',
                                                     owner=ontario))