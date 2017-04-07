"""Database interface module.

app/db.py
"""
# standard imports
import os
import sqlite3
from sqlite3 import Error
from ast import literal_eval

# 3rd party imports
from termcolor import cprint

# local imports
from app.room import Office, Living
from app.person import Staff, Fellow


def create_connection(database):
    """Create a database connection to a given db."""
    try:
        if not os.path.exists(database):
            print('{0} database does not exist'.format(database))
        else:
            conn = sqlite3.connect(database)
            return conn
    except Error as e:
        print('An error occurred: {0}'.format(e.args[0]))


def load_schema(db, db_schema='databases/amity_default.sql'):
    """Create database structure."""
    try:
        if not os.path.exists(db):
            raise Exception('Database {0} does not exist'.format(db))
        if not os.path.exists(db_schema):
            raise Exception('Schema {0} does not exist'.format(db_schema))
    except Exception as e:
        return e
    else:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            with open(db_schema, 'rt') as f:
                schema = f.read()
            cur.executescript(schema)


def load(rooms, persons, cur):
    """Load state to application."""
    load_office(rooms['offices'], cur)
    load_living(rooms['livingspaces'], cur)
    load_staff(persons['staff'], cur)
    load_fellow(persons['fellows'], cur)
    return 'Operation complete'


def save_office(dictoffice, cur):
    """Save office rooms data into database table offices."""
    # check for data existence
    try:
        if dictoffice:
            cur.execute('''SELECT COUNT(*) FROM offices''')
            records = cur.fetchone()[0]
            # some records exist
            if not records == 0:
                # delete existing records to avoid duplicate records
                cur.execute('''DELETE FROM offices''')
            # save current records
            for obj in list(dictoffice.values()):
                cur.execute("""INSERT INTO offices(id, name, type, occupants,
                            MAX_CAPACITY)
                                VALUES(?, ?, ?, ?, ?)""",
                            (obj.id, obj.name, obj.type_, str(obj.occupants),
                             obj.MAX_CAPACITY))

    except Error as e:
        print('Error: {0}'.format(e))


def load_office(dictoffice, cur):
    """Load office rooms data to application."""
    cur.execute('''SELECT COUNT(*) FROM offices''')
    records_count = cur.fetchone()[0]
    if not records_count == 0:
        cur.execute('''SELECT * FROM offices''')
        records = cur.fetchall()
        for record in records:
            dictoffice[record[1]] = Office(record[1], record[0],
                                           literal_eval(record[3]))
        cprint('offices data loaded successfully.', 'green')


def save_living(dictliving, cur):
    """Save living rooms data into database."""
    # check for data existence
    try:
        if dictliving:
            cur.execute('''SELECT COUNT(*) FROM livingspaces''')
            records = cur.fetchone()[0]
            # some records exist
            if not records == 0:
                # delete existing records to avoid duplicate records
                cur.execute('''DELETE FROM livingspaces''')
            # save current records
            for obj in list(dictliving.values()):
                cur.execute("""INSERT INTO livingspaces(id, name, type,
                            occupants, MAX_CAPACITY)
                            VALUES(?, ?, ?, ?, ?)""",
                            (obj.id, obj.name, obj.type_, str(obj.occupants),
                             obj.MAX_CAPACITY))

    except Error as e:
        print('Error: {0}'.format(e))


def load_living(dictliving, cur):
    """Load living rooms to application."""
    cur.execute('''SELECT COUNT(*) FROM livingspaces''')
    records_count = cur.fetchone()[0]
    if not records_count == 0:
        cur.execute('''SELECT * FROM livingspaces''')
        records = cur.fetchall()
        for record in records:
            dictliving[record[1]] = Living(record[1], record[0],
                                           literal_eval(record[3]))
        cprint('Living rooms data loaded successfully.', 'green')


def save_staff(dictstaff, cur):
    """Save staff persons data into database."""
    # check for data existence
    try:
        if dictstaff:
            cur.execute('''SELECT COUNT(*) FROM staff''')
            records = cur.fetchone()[0]
            # some records exist
            if not records == 0:
                # delete existing records to avoid duplicate records
                cur.execute('''DELETE FROM staff''')
            # save current records
            for obj in list(dictstaff.values()):
                cur.execute("""INSERT INTO staff(id, name, type, office_space)
                            VALUES(?, ?, ?, ?)""",
                            (obj.id, obj.name, obj.role, obj.office_space))
    except Error as e:
        print('Error: {0}'.format(e))


def load_staff(dictstaff, cur):
    """Load staff to application."""
    cur.execute('''SELECT COUNT(*) FROM staff''')
    records_count = cur.fetchone()[0]
    if not records_count == 0:
        cur.execute('''SELECT * FROM staff''')
        records = cur.fetchall()
        for record in records:
            dictstaff[record[1]] = Staff(record[1], record[0], record[3])
        cprint('staff data loaded successfully.', 'green')


def save_fellow(dictfellow, cur):
    """Save fellow persons data into database."""
    # check for data existence
    try:
        if dictfellow:
            cur.execute('''SELECT COUNT(*) FROM fellows''')
            records = cur.fetchone()[0]
            # some records exist
            if not records == 0:
                # delete existing records to avoid duplicate records
                cur.execute('''DELETE FROM fellows''')
            # save current records
            for obj in list(dictfellow.values()):
                cur.execute("""INSERT INTO fellows(id, name, type,
                            office_space, living_space, accommodation)
                            VALUES(?, ?, ?, ?, ?, ?)""",
                            (obj.id, obj.name, obj.role, obj.office_space,
                             obj.living_space, obj.accommodation))

    except Exception as e:
        print('Error: {0}'.format(e))


def load_fellow(dictfellow, cur):
    """Load staff to application."""
    cur.execute('''SELECT COUNT(*) FROM fellows''')
    records_count = cur.fetchone()[0]
    if not records_count == 0:
        cur.execute('''SELECT * FROM fellows''')
        records = cur.fetchall()
        for record in records:
            dictfellow[record[1]] = Fellow(record[1], record[0], record[3],
                                           record[5], record[4])
        cprint('Fellows data loaded successfully.', 'green')
