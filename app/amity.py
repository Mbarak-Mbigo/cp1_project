"""Amity main module.

app/amity.py

"""
# imports
from random import choice
import sqlite3 as lite
import os

# 3rd party imports
from termcolor import cprint

# local imports
from app.room import Office, Living
from app.person import Staff, Fellow
from app import db


class Amity(object):
    """Docstring for Amity."""

    rooms = {
        'offices': {},
        'livingspaces': {}
    }

    persons = {
        'staff': {},
        'fellows': {}
    }

    def create_room(self, rooms, room_type='OFFICE'):
        """Create room(s).

        create_room <room_name>... - Creates rooms in Amity.
        Using this command I should be able to create as
        many rooms as possible by specifying multiple room
         names after the create_room command.
        Args:
            type: type of room (office|living).
            rooms: A list of room names (any string)
        Returns:
            Room(s) created.
        Raises:
            TypeError: if rooms not a list.
            ValueError: if rooms not strings
            ValueError: if room_type type not in (office| living).
        """
        try:
            # check room type within domain
            if room_type not in ["office", "living", "OFFICE", "LIVING"]:
                raise ValueError("\nInvalid room type:\
                        {0}, should be office or living".format(room_type))
            # check room names given as a list
            elif not isinstance(rooms, list):
                return(rooms)
                raise TypeError("Provide a list of room name(s)")
            # check room names are strings
            elif len(rooms) == 0 or not all(isinstance(
                    x, str) for x in rooms):
                raise ValueError("Invalid room name, only strings accepted")

        except (ValueError, TypeError) as e:
            return e
        else:

            return self.add_room(rooms, room_type)

    def add_room(self, rooms, room_type):
        """Create and add room(s) to Amity."""
        status = []
        if room_type.upper() == "OFFICE":
            for room in rooms:
                if room not in self.rooms['offices'].keys():
                    self.rooms['offices'][room.upper()] = Office(room.upper())
                else:
                    status.append(room.upper())
            if len(status) == 0:
                return 'Room(s) ' + ', '.join(rooms) + ' Created successfully'
            else:
                return 'Rooms(s) ' + ', '.join(status) + ' already exists'
        else:
            for room in rooms:
                if room not in self.rooms['livingspaces'].keys():
                    self.rooms['livingspaces'][room.upper()] = Living(room.upper())
                else:
                    status.append(room.upper())
            if len(status) == 0:
                return 'Room(s) ' + ', '.join(rooms) + ' Created successfully'
            else:
                return 'Rooms(s) ' + ', '.join(status) + ' already exists'

    def add_person(self, name, role='FELLOW', accommodation='N'):
        """Create a person, add to system, allocate to random room.

        add_person <person_name> <FELLOW|STAFF> [wants_accommodation] -
        Adds a person to the system and allocates the person to a random room.
        wants_accommodation here is an optional argument which can be
        either Y or N.
        The default value if it is not provided is N.
        Args:
            name: person name (string)
            role: person role (FELLOW | STAFF)
            wants_accommodation: ('Y' | 'N')
        Returns:
            Name of person added
        Raises:
            ValueError: if name not string
            ValueError: if roleƒ not in specified domain
            ValueError: if wants_accommodation not in specified domain
            PermissonError: if role is STAFF and wants_accommodation is 'Y'
        """
        try:
            # name given not string
            if not isinstance(name, str):
                raise ValueError('Person name can only be a string')
            # person already exists
            elif name.upper() in (self.persons['staff'].keys()) or name in\
                    (self.persons['fellows'].keys()):
                raise ValueError('Person: {0} already exists'.format(name))
            # Role not in domain
            elif role not in ['staff', 'fellow', 'STAFF', 'FELLOW']:
                raise ValueError('Person role can either be STAFF or FELLOW')
            # accommodation not within specified domain
            elif accommodation not in ['y', 'Y', 'n', 'N']:
                raise ValueError("Accommodation can either be 'Y' or 'N' ")

        except (ValueError, PermissionError) as e:
            return e
        else:
            # create person
            # staff wants accommodation
            if role.upper() == 'STAFF':
                self.persons['staff'][name.upper()] = Staff(name.upper())
            else:
                self.persons['fellows'][name.upper()] = Fellow(
                    name.upper(), None, None, accommodation)
            # allocate room

            return self.allocate_room(name.upper(), role, accommodation)

    def reallocate_person(self, person_id, new_room_name):
        """Reallocate a person from one room to another.

        reallocate_person <person_identifier> <new_room_name> -
        Reallocate the person with person_identifier to new_room_name.

        Args:
            person_id: a valid person id
            new_room_name: a valid room

        Returns:
            Reallocation status
        """
        try:
            current_room = None
            # get new room
            all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
            reallocate_room = all_rooms.get(new_room_name.upper())
            # get person
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            person = next((person for person in list(all_pple.values()) if person.id == int(person_id)), None)
            # room to reallocate not found
            if not reallocate_room:
                raise ValueError('{0} is\
                 not a room in the system'.format(new_room_name))
            # person not found
            if not person:
                raise ValueError('No person with id {0}'.format(person_id))

        except ValueError as e:
            return e

        else:
            # capture staff reallocate to living space'
            if reallocate_room.type_ == 'LIVING' and person.role == 'FELLOW' and not person.living_space:
                return 'Cannot reallocate unallocated person'
            if reallocate_room.type_ == 'LIVING' and person.role == 'STAFF':
                return "Cannot reallocate staff to living space"

            if reallocate_room.type_ == 'OFFICE' and not person.office_space:
                return "Allocate office space before reallocating"
            else:
                current_room = self.rooms['offices'][person.office_space]
                if current_room == reallocate_room:
                    return "Cannot reallocate to the same Office"
                else:
                    current_room.occupants.remove(person.name)
                    reallocate_room.occupants.append(person.name)
                    person.office_space = (reallocate_room.name)
                    return "Reallocation of office space successful."

            if reallocate_room.type_ == 'LIVING' and not person.living_space:
                return "Allocate living space before reallocating"
            else:
                if current_room == reallocate_room:
                    return 'Cannot reallocate to the same Living space.'
                else:
                    current_room = self.rooms['livingspaces'][person.living_space]
                    current_room.occupants.remove(person.name)
                    reallocate_room.occupants.append(person.name)
                    person.living_space = reallocate_room.name
                    return "Reallocation of living space successful."

    def load_people(self, filename):
        """"Add people to rooms from a txt file.

        filename: txt file  values: person names and details
        Scenario:
            File does not exist
                raise exception file not exist
            File Exists
                file type not txt
                    raise exception
                file type txt
                    No data
                        Raise exception
                    Data exists
                            Unkown format
                                raise exception
                            data format okay
                                perform load operation

        """
        try:
            filepath = ''.join(['data/', filename])
            if not os.path.exists(filepath):
                raise FileNotFoundError("Loading file not found")
            elif os.stat(filepath).st_size == 0:
                return "File is empty"

        except FileNotFoundError as e:
            return e
        else:
            with open(filepath) as f:
                for line in f:
                    line = line.strip()
                    person_details = line.split(' ')
                    name = person_details[0] + ' ' + person_details[1]
                    person_type = person_details[2]
                    if person_details[-1] == "Y":
                        self.add_person(name, person_type, person_details[-1])
                    else:
                        self.add_person(name, person_type)
                return "Loading operation successful"

    def print_allocations(self, outfile=None):
        """"Print to the screen a list of rooms and the people allocated.

        if outfile provided output list to the file  as well
        Scenario:
        No rooms or rooms available but no allocations yet
            raise exception
        Rooms available allocations okay
            outfile provided
                print to screen and file
            outfile not provided
                print to screen

        """
        try:
            if not any(self.rooms):
                raise ValueError("No rooms available")
            else:
                occupied_offices = [o for o in list(
                    self.rooms['offices'].values()) if len(o.occupants) > 0]
                occupied_living = [l for l in list(
                    self.rooms['livingspaces'].values()) if len(l.occupants) > 0]
                if len(occupied_offices) == 0 and len(occupied_living) == 0:
                    return("\nThere are no allocations\n")

        except ValueError as e:
            return e
        else:
            if outfile:
                filepath = ''.join(['data/', outfile])
            else:
                filepath = outfile
            if filepath:
                with open(filepath, "w") as f:
                    for room in (occupied_offices + occupied_living):
                        f.write(room.name + '\n')
                        f.write(", ".join(room.occupants))
                        f.write('\n')
            print("ALLOCATIONS")
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            for room in (occupied_offices + occupied_living):
                print("Room: {0} Type: {1}".format(room.name, room.type_))
                print("--------------------------------")
                for name in room.occupants:
                    person = all_pple[name]
                    print('{0} {1} {2}'.format(person.id, person.name, person.role))
                print("\n\n")

    def print_unallocated(self, outfile=None):
        """"
        print a list of all unallocated people on the screen
        if outfile is provided, output the list to the file

        Scenario:
        No person
            respond accordingly
        People available
            No one unallocated
                handle accordingly
            office
                fellows
                staff
            living
                fellows

        outfile provided
            output to file too.
        """
        try:
            if not any(dict(self.persons['staff'], **self.persons['fellows'])):
                raise ValueError("No people in the system")

        except ValueError as e:
            return e
        else:
            all_persons = list(self.persons['staff'].values()) + list(
                self.persons['fellows'].values())
            unallocated_office = [
                p for p in all_persons if p.office_space is None]
            unallocated_living = [
                l for l in all_persons if l.role is 'FELLOW' and
                l.accommodation is 'Y' and l.living_space is None]
            if outfile:
                filepath = ''.join(['data/', outfile])
            else:
                filepath = outfile

            if filepath:
                with open(filepath, 'w') as f:
                    if unallocated_office:
                        f.write("UNALLOCATED OFFICE SPACE \n")
                        for person in unallocated_office:
                            f.write(str(person))
                            f.write('\n')
                    if unallocated_living:
                        f.write("UNALLOCATED LIVING SPACE \n")
                        for person in unallocated_living:
                            f.write(str(person))
                            f.write('\n')

            print("\nUNALLOCATED OFFICE SPACE")
            print("-----------------------------------")
            for person in unallocated_office:
                print(person)
            print("\nUNALLOCATED LIVING SPACE")
            print("-----------------------------------")
            for person in unallocated_living:
                print(person)
            return 'Operation successful.'

    def print_room(self, room_name):
        """"Given a room name, print all the people allocated to that room.

        Scenarios:
        room not in pool
            raise exception
        room in pool
            no allocations
                handle accordingly
            allocations available
                display allocations
        """
        try:
            all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
            if not all_rooms.get(room_name.upper()):
                raise ValueError("No room with name: {0}".format(room_name))
        except ValueError as e:
            return e
        else:
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            room = all_rooms[room_name.upper()]
            print('\nRoom: {0}'.format(room.name))
            print('----------------------------------')
            if not room.occupants:
                cprint('No allocations yet', 'red')
            else:
                for name in room.occupants:
                    person = all_pple[name]
                    print('{0} {1} {2}'.format(
                        person.id, person.name, person.type_))
                print('\n')

    def save_state(self, database=None):
        """"Persist all data in a db.

        if db name is new,
            create db,
                structure using a schema,
                populate with app data
        db already exists:
            update data:
                could delete  and recreate
                or fetch and update
        return status
        """
        try:
            conn = None
            if database:
                dbpath = ''.join(['databases/', database])
            else:
                dbpath = ''.join(['databases/', 'amity_default.db'])
            # database does not exist
            if not os.path.exists(dbpath):
                lite.connect(dbpath)
                db.load_schema(dbpath)
                print('{0} Created successfully'.format(dbpath))
            conn = db.create_connection(dbpath)

        except Exception as e:
            return e
        else:
            if conn:
                with conn:
                    cur = conn.cursor()
                    print('Updating records...')
                    db.save_office(self.rooms['offices'], cur)
                    db.save_living(self.rooms['livingspaces'], cur)
                    db.save_staff(self.persons['staff'], cur)
                    db.save_fellow(self.persons['fellows'], cur)
                    print('Done...')
        finally:
            if conn:
                conn.close()

    def load_state(self, database=None):
        """Load data from the provided database into the application."""
        # check existence of database
        """
        if does not exist
            return err msg

        if exists,
            check if has valid data
                no?
                    return msg
                else:
                    load data from db to app

        """
        try:
            if database:
                dbpath = ''.join(['databases/', database])
            else:
                dbpath = ''.join(['databases/', 'amity_default.db'])

            # check db existence
            if not os.path.exists(dbpath):
                raise FileNotFoundError(
                    '{0} database not found'.format(database))


        except FileNotFoundError as e:
            return e
        else:
            # db exists
            conn = db.create_connection(dbpath)
            if conn:
                cur = conn.cursor()
                print('Loading data....')
                db.load_office(self.rooms['offices'], cur)
                db.load_living(self.rooms['livingspaces'], cur)
                db.load_staff(self.persons['staff'], cur)
                db.load_fellow(self.persons['fellows'], cur)
                print('Data loaded successfully')
            else:
                print('Invalid Connection')
        finally:
            if conn:
                conn.close()

    # added functionality

    def print_available_space(self):
        """Print all rooms and spaces available on each room.

        args: None
        Returns: un allocated space
        Raise:
            ValueError: if no room space available

        """
        try:
            all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
            if not any(all_rooms):
                raise ValueError("No room space available")

        except ValueError as e:
            print('\nStatus: {0}'.format(e))
        else:
            office_space = [o for o in list(self.rooms[
                'offices'].values()) if len(o.occupants) < 6]
            living_space = [l for l in list(self.rooms[
                'livingspaces'].values()) if len(l.occupants) < 4]
            print("\nAVAILABLE ROOMS:")
            print('Room:' + "   " + 'Space')
            print('Office Space:')
            print('------------------------')
            for room in office_space:
                print('{0} {1}'.format(room.name, 6 - len(room.occupants)))
            print('\n\nLiving Space')
            print('------------------------')
            for room in living_space:
                print('{0} {1}'.format(room.name, 4 - len(room.occupants)))
            print('\n')

    # # Helper functions
    def allocate_room(self, name, role, accommodation):
        """"Allocate room to person."""
        # get person
        if role.upper() == 'STAFF':
            person = self.persons['staff'][name]
        else:
            person = self.persons['fellows'][name]

        # get office room
        room_key = self.get_random_room('office')
        if room_key:
            room = self.rooms['offices'][room_key]
            if room:
                # room capacity not exceeded
                if not room.is_full():
                    person.office_space = room_key
                    room.occupants.append(person.name)

        # get living room
        if person.role is 'STAFF' and accommodation is 'Y':
            return 'Staff cannot request for accommodation'
        elif person.role == 'FELLOW' and person.accommodation == 'Y':
            room_key = self.get_random_room('living')
            if room_key:
                room = self.rooms['livingspaces'][room_key]
                if room:
                    # living room capacity not exceeded
                    if not room.is_full():
                        person.living_space = room_key
                        room.occupants.append(person.name)

        if person.role is 'STAFF' and person.office_space:
            return "{0} added:\nOffice space assigned successfully".format(person.name)
        elif person.role is 'FELLOW' and person.office_space and person.living_space:
            return "{0} added:\nOffice and Living spaces assigned successfullly".format(person.name)
        elif person.role is 'FELLOW' and person.office_space and not person.living_space:
            return "{0} added:\nOnly office space allocated".format(person.name)
        elif person.role is 'FELLOW' and not person.office_space and not person.living_space:
            return '{0} added:\nNo allocations made'.format(person.name)
        elif person.role is 'FELLOW' and not person.office_space and person.living_space:
            return '{0} added:\nLiving space assigned successfully'.format(person.name)
        elif person.role is 'STAFF' and not person.office_space:
            return "{0} added:\nOffice space not assigned".format(person.name)

    def get_random_room(self, room_type, current_room=None):
        """Return a room name or None."""
        try:
            # room type not  in domain
            if room_type not in ['office', 'living', 'OFFICE', 'LIVING']:
                raise ValueError("Room type can only be office or living")
            # room name not string
            elif not isinstance(current_room, str) and\
                    current_room is not None:
                raise ValueError("Room name must be a string")
        except ValueError as e:
            return e
        else:
            # check if there are rooms
            rooms = None
            if room_type.upper() == 'OFFICE':
                if not any(self.rooms['offices']):
                    return None
                else:
                    rooms = list(self.rooms['offices'].keys())
                    if current_room:
                        rooms.remove(current_room)
                    return choice(rooms)
            else:
                if not any(self.rooms['livingspaces']):
                    return None
                else:
                    rooms = list(self.rooms['livingspaces'].keys())
                    if current_room:
                        rooms.remove(current_room)
                    return choice(rooms)
