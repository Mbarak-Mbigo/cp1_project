"""Database interface module.

app/db.py
"""
import os
import sqlite3
from sqlite3 import Error


def create_connection(database):
    """Create a database connection to a given db."""
    try:
        if not os.path.exists(database):
            print('Database does not exist.')
        else:
            conn = sqlite3.connect(database)
            return conn
    except Error as e:
        print('An error occurred: {0}'.format(e.args[0]))
        return None


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
        return 'Database ready for loading data'

"""
check if database exists:
    does not exist
        (run schema script)
        create database
            create tables
        on successful execution
            load save data to database if need be

    does exist
        update database
        notify on successful update
        or
        read data to application
        notify on successful loading

    create_db
    create_table
    insert data
    select data
    update data
    delete data

TABLES
    person:
        id, name, type, office_space

    staff:
        id, name, type, office_space
    fellow:
        id, name, type, office_space, living_space, accommodation


    room:
        id, name, type, occupants, max_capacity

    offices:
        id, name, type, occupants, max_capacity
    living:
        id, name, type, occupants, max_capacity

        occupants: a possible table
"""


