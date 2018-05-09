#!/usr/env python
#
# Migrations for the Signman DB. This is an ugly hack and really needs a schema version field in the DB.
# If you want to add a migration, add it as new function and add in to the "migrations" list.
#
# Documentation: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations
#

import sys
sys.path.append("./deps")

import peewee
from playhouse.migrate import *
from config import *

def version2():
    description = CharField(default="< migrated >")

    migrate(
        migrator.add_column('URL', 'description', description)
    )


# Add migrations here
migrations = [
    version2
]


my_db = SqliteDatabase(DB_DATA_DIR)
migrator = SqliteMigrator(my_db)

for migration in migrations:

    try:
        print "Applying migration '%s'" % migration.__name__
        migration()
        print "Done"

    except peewee.OperationalError as e:
        print "Already applied \nResult when trying to apply: %s" % e

