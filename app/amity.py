"""Amity main module.

app/amity.py

"""
# imports
from random import choice
import sqlite3 as lite
import os

# 3rd party imports
from termcolor import cprint
from tabulate import tabulate

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

    def create_room(self, rooms, type_='OFFICE'):
        """Create rooms in Amity.

        Args:
            type_: type of room (office|living).
            rooms: A list of room names (any string)
        Returns:
            Room(s) created.
        Raises:
            ValueError: if rooms not strings
            ValueError: if room_type type not in (office| living).
        """
        try:
            # check room type within domain
            if type_ not in ["office", "living", "OFFICE", "LIVING"]:
                cprint('Invalid type: {0}, should be office or living.'
                       .format(type_), 'red')
                raise ValueError('Invalid room type: {0}'.format(type_))

            if not all(isinstance(room, str) for room in rooms):
                cprint('Room names can only be strings', 'red')
                raise TypeError('Invalid room name type')

        except (ValueError, TypeError) as e:
            return e

        else:
            return self._add_room(rooms, type_)

    def _add_room(self, rooms, room_type):
        """Create and add room(s) to Amity."""
        if room_type.upper() == "OFFICE":
            exists = self._add_office(rooms)
        else:
            exists = self._add_living(rooms)

        if not exists:
            cprint('Room(s) ' + ', '.join(rooms) + ' Created successfully',
                   'green')
            return 'Success'
        else:
            cprint('Rooms Created:{0}'
                   .format([room for room in rooms if room not in exists]),
                   'white')
            cprint('Room(s) ' + ', '.join(exists) + ' already exists', 'red')
            return "Can't recreate existing rooms"

    def _add_office(self, rooms):
        """Add office rooms to system."""
        exists = []
        for room in rooms:
            if self._room_exists(room):
                exists.append(room)
            else:
                self.rooms['offices'][room.upper()] = Office(room.upper())
        return exists

    def _add_living(self, rooms):
        """Add living rooms to system."""
        exists = []
        for room in rooms:
            if self._room_exists(room):
                exists.append(room)
            else:
                self.rooms['livingspaces'][room.upper()] = Living(room.upper())
        return exists

    def _room_exists(self, room):
        """Return true if room exists."""
        all_rooms = dict(self.rooms['offices'], **self.rooms['livingspaces'])
        if room.upper() in all_rooms.keys():
            return True
        else:
            return False

    def add_person(self, name, role='FELLOW', accommodation='N'):
        u"""Create a person, add to system, allocate to random room.

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
                raise ValueError(cprint('Person name can only be a string',
                                        'red'))
            # person already exists
            elif name.upper() in self.persons['staff'].keys() or\
                    name.upper() in self.persons['fellows'].keys():
                cprint('Person: {0} already exists'.format(name), 'red')
                raise ValueError('Person: {0} already exists'.format(name))
            # Role not in domain
            elif role not in ['staff', 'fellow', 'STAFF', 'FELLOW']:
                cprint('Person role can either be STAFF or FELLOW', 'red')
                raise ValueError('Person role can either be STAFF or FELLOW')
            # accommodation not within specified domain
            elif accommodation not in ['y', 'Y', 'n', 'N']:
                cprint("Accommodation can either be 'Y' or 'N' ", 'red')
                raise ValueError("Accommodation can either be 'Y' or 'N' ")

        except (ValueError, PermissionError) as e:
            return e
        else:
            # create person
            if role.upper() == 'STAFF':
                self.persons['staff'][name.upper()] = Staff(name.upper())
                cprint('Staff: {0} added successfully.'.format(name), 'green')
            else:
                self.persons['fellows'][name.upper()] = Fellow(
                    name.upper(), None, None, accommodation)
                cprint('Fellow: {0} added successfully.'.format(name), 'green')
            if role.upper() == 'STAFF' and accommodation == 'Y':
                cprint('Staff cannot request for accommodation', 'red')
                return 'Staff cannot request for accommodation'
            # allocate person
            else:
                return self.allocate_room(name)

    def allocate_room(self, name=None):
        """Allocate room to person."""
        try:
            person = None
            unallocated = []
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            if all_pple:
                if name:
                    person = all_pple[name.upper()]
                    unallocated.append(person)
                else:
                    unallocated = [person for person in list(
                        all_pple.values()) if not person.office_space]
                    unallocated.extend([person for person in list(
                        self.persons['fellows'].values()) if not
                        person.living_space and person.accommodation == 'Y'])
            # person does not exist
            if not unallocated:
                if name and not person:
                    cprint('Person: {0} does not exist'.format(name), 'red')
                    raise ValueError('Person: {0} does not exist'.format(name))
                else:
                    cprint('No person to allocate', 'red')
                    raise ValueError('No person to allocate')
        except ValueError as e:
            return e
        except KeyError as e:
            cprint('Person: {0} does not exist'.format(name), 'red')
            return e
        else:
            # person exists
            for person in unallocated:
                if person.role == 'STAFF' and not person.office_space:
                    self.allocate_office(person)
                elif person.role == 'STAFF' and person.office_space:
                    cprint('Staff: {0} already allocated office space,'
                           'did you want to reallocate?'.format(person.name),
                           'red')
                    return 'Staff: {0} already allocated office space,'\
                        'did you want to reallocate?'.format(person.name)
                else:
                    if person.role == 'FELLOW' and not person.office_space and\
                            not person.living_space:
                        self.allocate_office(person)
                        if person.accommodation == 'Y':
                            self.allocate_living_space(person)
                    elif person.role == 'FELLOW' and not person.living_space:
                        self.allocate_living_space(person)
                    else:
                        cprint('Fellow:{0} already allocated, did you want to'
                               'realloate?'.format(person.name))
                        return 'Fellow:{0} already allocated, did you want to'\
                               'realloate?'.format(person.name)

    def allocate_office(self, person):
        """Allocate office space.

        check rooms exist
        # how about exist but full?
        """
        if not any(self.rooms['offices']):
            cprint('No office rooms to allocate.', 'red')
        else:
            office = self.get_random_room('OFFICE')
            if office:
                person.office_space = office.name
                office.occupants.append(person.name)
            cprint('Office space allocated successfully.', 'green')

    def allocate_living_space(self, person):
        """Allocate living space."""
        # get living room
        if not any(self.rooms['livingspaces']):
            cprint('No Living rooms to allocate.', 'red')
        else:
            livingroom = self.get_random_room('LIVING')
            if livingroom:
                person.living_space = livingroom.name
                livingroom.occupants.append(person.name)
            cprint('Living space allocated successfully.', 'green')

    def allocate_staff(self):
        pass

    def allocate_fellow(self):
        pass

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
            all_rooms = dict(
                self.rooms['offices'], **self.rooms['livingspaces'])
            # get room to reallocate
            if any(all_rooms):
                reallocate_room = all_rooms.get(new_room_name.upper())
            else:
                raise ValueError(cprint('No rooms in the system yet', 'red'))
            # room to reallocate not found
            if not reallocate_room:
                raise ValueError(cprint('{0} is not a room in the system'
                                        .format(new_room_name), 'red'))
            # get person
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            if any(all_pple):
                person = next((person for person in list(
                    all_pple.values()) if person.id == int(person_id)), None)
            else:
                raise ValueError(cprint('No people in the system yet', 'red'))
            # person not found
            if not person:
                raise ValueError(cprint('No person with id {0}'
                                        .format(person_id), 'red'))

        except ValueError as e:
            return e

        else:
            # person found reallocate room found
            if reallocate_room.type_ == 'OFFICE':
                return self.reallocte_office(person, reallocate_room)
            else:
                return self.reallocate_living_space(person, reallocate_room)

    def reallocate_staff(self):
        pass

    def reallocate_fellow(self):
        pass

    def reallocte_office(self, person, reallocate_room):
        """Reallocate office space."""
        if not person.office_space:
            return cprint('Allocate office space before reallocating.', 'red')
        else:
            current_office = self.rooms['offices'][person.office_space]
            if current_office == reallocate_room:
                return cprint('Cannot reallocate to the same office', 'red')
            elif current_office.type_ is not reallocate_room.type_:
                return cprint('Cannot reallocate from office to living', 'red')
            else:
                current_office.occupants.remove(person.name)
                reallocate_room.occupants.append(person.name)
                person.office_space = reallocate_room.name
                print('my reallocated office space: {0}'.format(person.office_space))
                cprint("Reallocation of office space successful.", 'green')

    def reallocate_living_space(self, person, reallocate_room):
        """Reallocate living space."""
        if person.role == 'STAFF':
            return cprint('Cannot reallocate staff to living space', 'red')
        elif person.role == 'FELLOW' and not person.living_space:
            return cprint('Allocate living space before reallocateding', 'red')
        else:
            current_living = self.rooms['livingspaces'][person.living_space]
            if current_living == reallocate_room:
                return cprint('Cannot reallocate to same living space', 'red')
            elif current_living.type_ is not reallocate_room.type_:
                return cprint('Cannot reallocate from living to office', 'red')
            else:
                current_living.occupants.remove(person.name)
                reallocate_room.occupants.append(person.name)
                person.living_space = reallocate_room.name
                return cprint('Reallocation to living space successful.',
                              'green')

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
                raise FileNotFoundError(cprint("Loading file not found",
                                               'red'))
            elif os.stat(filepath).st_size == 0:
                return cprint("File is empty", 'red')

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
                return cprint("Loading operation successful", 'white')

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
                raise ValueError(cprint("No rooms available", 'red'))
            else:
                occupied_offices = [o for o in list(
                    self.rooms['offices'].values()) if len(o.occupants) > 0]
                occupied_living = [l for l in list(
                    self.rooms['livingspaces'].values()) if len(
                        l.occupants) > 0]
                if len(occupied_offices) == 0 and len(occupied_living) == 0:
                    return(cprint("\nThere are no allocations\n", 'red'))

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
            print(cprint("ALLOCATIONS", 'white'))
            all_pple = dict(self.persons['staff'], **self.persons['fellows'])
            for room in (occupied_offices + occupied_living):
                print(cprint("Room: {0} Type: {1}".format(
                    room.name, room.type_), 'green'))
                print("--------------------------------")
                print_data = []
                for name in room.occupants:
                    person = all_pple[name]
                    print_data.append([person.id, person.name, person.role])
                print(tabulate(print_data, headers=['ID', 'NAME', 'TYPE'],
                               tablefmt='orgtbl'))
                print("--------------------------------")
            return

    def print_unallocated(self, outfile=None):
        """"Print a list of all unallocated people.

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
                raise ValueError(cprint("No people in the system", 'red'))

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

            cprint("\nUNALLOCATED OFFICE SPACE", 'green')
            print("-----------------------------------")
            print_data = []
            if unallocated_office:
                for person in unallocated_office:
                    print_data.append([person.id, person.name, person.role])
                print(tabulate(print_data, headers=['ID', 'NAME', 'TYPE'],
                               tablefmt='orgtbl'))
                print("-----------------------------------")
                cprint("\nUNALLOCATED LIVING SPACE", 'green')
                print("----------------------------------------------------")
            else:
                cprint('No unallocated office space', 'red')
            print_data = []
            if unallocated_living:
                for person in unallocated_living:
                    print_data.append([person.id, person.name, person.role,
                                      person.accommodation])
                print(tabulate(print_data, headers=['ID', 'NAME', 'TYPE',
                               'ACCOMMODATION'],
                               tablefmt='orgtbl'))
                print("----------------------------------------------------")
            else:
                cprint('No unallcoated living space', 'red')
            return cprint('Operation successful.', 'white')

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
            all_rooms = dict(
                self.rooms['offices'], **self.rooms['livingspaces'])
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
                print_data = []
                for name in room.occupants:
                    person = all_pple[name]
                    print_data.append([person.id, person.name, person.role])
                print(tabulate(print_data, headers=['ID', 'NAME', 'TYPE'],
                               tablefmt='orgtbl'))
                print('----------------------------------')

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
        # if db not specified pick latest database
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
            conn = None
            if database:
                dbpath = ''.join(['databases/', database])
            else:
                dbpath = ''.join(['databases/', 'amity_default.db'])
                # dbpath not given, get latest db back up
                choice_db = 'databases/amity_default.db'
                for file in os.listdir('databases'):
                    if file.endswith('.db'):
                        current_db = ''.join(['databases/', file])
                        if os.stat(current_db).st_mtime >= os.stat(
                                choice_db).st_mtime:
                            choice_db = current_db
                dbpath = choice_db

            # check db existence
            if not os.path.exists(dbpath):
                raise FileNotFoundError(cprint(
                    '{0} database not found\n'.format(database), 'red'))

        except FileNotFoundError as e:
            return e
        else:
            # db exists
            conn = db.create_connection(dbpath)
            if conn:
                all_pple = dict(self.persons['staff'],
                                **self.persons['fellows'])
                all_rooms = dict(self.rooms['offices'],
                                 **self.rooms['livingspaces'])
                if any(all_pple) or any(all_rooms):
                    cprint('Current applicaton data will be overwriten!\n',
                           'red')
                    choice = input('Enter:"y" to continue, "n" to Cancel ')
                    while choice not in ['n', 'N', 'y', 'Y']:
                        cprint('Invalid choice:{0}'.format(choice), 'red')
                        choice = input('Enter:"y" to continue,'
                                       '"n" to Cancel: ')
                    else:
                        if choice in ['y', 'Y']:
                            print('updating... \n')
                            cur = conn.cursor()
                            cprint(db.load(self.rooms, self.persons, cur),
                                   'white')
                        elif choice in ['n', 'N']:
                            cprint('\nOperation cancelled', 'green')
                else:
                    cur = conn.cursor()
                    cprint(db.load(self.rooms, self.persons, cur), 'white')
            else:
                print(cprint('Invalid Connection', 'red'))
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
            all_rooms = dict(
                self.rooms['offices'], **self.rooms['livingspaces'])
            if not any(all_rooms):
                raise ValueError("No room space available")

        except ValueError as e:
            cprint('\nStatus: {0}'.format(e), 'red')
        else:
            office_space = [room for room in list(self.rooms[
                'offices'].values()) if len(room.occupants) < 6]
            living_space = [room for room in list(self.rooms[
                'livingspaces'].values()) if len(room.occupants) < 4]
            cprint("\nAVAILABLE SPACE IN ROOMS:", 'green')
            if office_space:
                cprint('Office Space:', 'green')
                print('--------------------')
                print_data = []
                for room in office_space:
                    print_data.append([room.name, 6 - len(room.occupants)])
                print(tabulate(print_data, headers=['ROOM', 'SPACE'],
                               tablefmt='orgtbl'))
            else:
                cprint('No office space available', 'red')
            if living_space:
                print('--------------------')
                print('\nLiving Space')
                print_data = []
                print('--------------------')
                for room in living_space:
                    print_data.append([room.name, 4 - len(room.occupants)])
                print(tabulate(print_data, headers=['ROOM', 'SPACE'],
                               tablefmt='orgtbl'))
                print('--------------------')
            else:
                cprint('No living space available', 'red')

    # # Helper functions

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
                # No rooms in system yet
                if not any(self.rooms['offices']):
                    return None
                else:
                    rooms = [room for room in list(
                        self.rooms['offices'].values()) if not room.is_full()]
                    if current_room and current_room in rooms:
                        rooms.remove(current_room)
            else:
                if not any(self.rooms['livingspaces']):
                    return None
                else:
                    rooms = [room for room in list(self.rooms[
                        'livingspaces'].values()) if not room.is_full()]
                    if current_room and current_room in rooms:
                        rooms.remove(current_room)
            if len(rooms):
                return choice(rooms)
            else:
                return None
